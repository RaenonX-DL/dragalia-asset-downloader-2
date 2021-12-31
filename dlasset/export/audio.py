"""Implementations for exporting raw assets."""
import json
import os.path
import re
import shutil
import subprocess
from typing import TYPE_CHECKING

from dlasset.config import AssetAudioTask
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start
from dlasset.manage import get_asset_paths
from dlasset.utils import concurrent_run, concurrent_run_no_return

if TYPE_CHECKING:
    from dlasset.manifest import Manifest, ManifestRawEntry

__all__ = ("export_audio",)


def export_single_awb_subsong(
        env: Environment, executable_path: str, audio_entry: "ManifestRawEntry", awb_file_path: str,
        subsong_idx: int, has_name: bool
) -> None:
    """Export a subsong of an audio."""
    export_path = os.path.join(
        env.config.audio_task.export_dir,
        audio_entry.name,
        "?n.wav" if has_name else "?03s.wav"
    )

    args_subsong_args: list[str] = [
        executable_path,
        "-s",
        str(subsong_idx),
        "-i",
        "-o",
        export_path,
        awb_file_path,
    ]

    subprocess.run(args_subsong_args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def export_awb_subsongs(env: Environment, audio_entry: "ManifestRawEntry", awb_file_path: str) -> None:
    """Export the subsongs of ``awb_file_path``."""
    executable_path = os.path.join("lib", "vgmstream", "vgmstream")

    args_get_meta: list[str] = [
        executable_path,
        "-I",
        "-m",
        awb_file_path
    ]

    metadata = json.loads(subprocess.run(args_get_meta, stdout=subprocess.PIPE).stdout)

    has_name = metadata["streamInfo"]["name"] is not None
    subsong_count = metadata["streamInfo"]["total"]

    concurrent_run_no_return(
        export_single_awb_subsong,
        [
            [env, executable_path, audio_entry, awb_file_path, subsong_idx, has_name]
            for subsong_idx in range(subsong_count)
        ],
        env.config.paths.log
    )


def download_audio_to_temp(
        env: Environment, audio_entry: "ManifestRawEntry"
) -> tuple["ManifestRawEntry", str]:
    """
    Download the audio assets of ``audio_entry`` to the temp direcotry.

    Returns the audio entry
    """
    # Downloads the asset of ``audio_entry``, the return is useless here
    get_asset_paths(env, [audio_entry])

    original_asset_path = audio_entry.get_asset_path(env)
    target_asset_path = os.path.join(env.config.paths.temp, "audio", audio_entry.name)

    # Ensure the necessary directory exists
    os.makedirs(os.path.dirname(target_asset_path), exist_ok=True)
    shutil.move(original_asset_path, target_asset_path)

    return audio_entry, target_asset_path


def export_audio(env: Environment, manifest: "Manifest", ___: AssetAudioTask) -> None:
    """Export audio assets."""
    log_group_start("Audio exporting")

    audio_entries: list["ManifestRawEntry"] = [
        audio_entry
        for locale, audio_entries
        in manifest.get_raw_entry_with_regex(re.compile(r".*\.(awb|acb)"), is_master_only=False)
        for audio_entry
        in audio_entries
    ]

    files_for_export: list[tuple["ManifestRawEntry", str]] = []

    log("INFO", "Downloading audio assets...")

    # Download all audio first to ensure `acb` and `awb` files exist at the same time for later processing
    for audio_entry, audio_path in concurrent_run(
            download_audio_to_temp, [[env, audio_entry] for audio_entry in audio_entries], env.config.paths.log,
            key_of_call=lambda _, entry: entry.name
    ).values():
        # Skips pending-process for non-awb files
        if not audio_path.endswith(".awb"):
            continue

        files_for_export.append((audio_entry, audio_path))

    log("INFO", f"Found {len(files_for_export)} awb files to export.")

    for idx, (audio_entry, awb_path) in enumerate(files_for_export, start=1):
        progress = idx / len(files_for_export)

        log("INFO", f"Exporting audio ({idx} / {len(files_for_export)} - {progress:.2%}) - {awb_path}")

        export_awb_subsongs(env, audio_entry, awb_path)

    log_group_end()
