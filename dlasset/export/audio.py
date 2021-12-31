"""Implementations for exporting raw assets."""
import json
import os.path
import re
import shutil
# The usage of `subprocess` is safe
import subprocess  # nosec
import sys
from collections import namedtuple
from typing import TYPE_CHECKING

from dlasset.config import AssetAudioTask
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start, log_periodic
from dlasset.manage import get_asset_paths
from dlasset.utils import concurrent_run, concurrent_run_no_return

if TYPE_CHECKING:
    from dlasset.manifest import Manifest, ManifestRawEntry

__all__ = ("export_audio",)

AudioDownloadResult = namedtuple("AudioDownloadResult", ["awb_path", "manifest_entry"])


def export_single_awb_subsong(
        env: Environment, executable_path: str, download_result: AudioDownloadResult,
        subsong_idx: int, has_name: bool
) -> None:
    """Export a subsong of an audio."""
    if not env.config.audio_task:
        log("ERROR", "Attempt to export audio but audio task is not defined.")
        sys.exit(1)

    export_path = os.path.join(
        env.config.audio_task.export_dir,
        download_result.manifest_entry.name,
        "?n.wav" if has_name else "?03s.wav"
    )

    args_subsong_args: list[str] = [
        executable_path,
        "-s",
        str(subsong_idx),
        "-i",
        "-o",
        export_path,
        download_result.awb_path,
    ]

    subprocess.run(args_subsong_args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)  # nosec


def export_awb_subsongs(env: Environment, download_result: AudioDownloadResult) -> None:
    """Export the subsongs of ``awb_file_path``."""
    executable_path = os.path.join("lib", "vgmstream", "vgmstream")

    args_get_meta: list[str] = [
        executable_path,
        "-I",
        "-m",
        download_result.awb_path
    ]

    metadata = json.loads(subprocess.run(args_get_meta, stdout=subprocess.PIPE, check=True).stdout)  # nosec

    has_name = metadata["streamInfo"]["name"] is not None
    subsong_count = metadata["streamInfo"]["total"]

    concurrent_run_no_return(
        export_single_awb_subsong,
        [
            [env, executable_path, download_result, subsong_idx, has_name]
            for subsong_idx in range(subsong_count)
        ],
        env.config.paths.log
    )


def download_audio_to_temp(
        env: Environment, audio_entry: "ManifestRawEntry"
) -> AudioDownloadResult:
    """Download the audio assets of ``audio_entry`` to the temp direcotry."""
    log_periodic("INFO", "Downloading audio assets...", period=3)

    # Downloads the asset of ``audio_entry``, the return is useless here
    get_asset_paths(env, [audio_entry])

    original_asset_path = audio_entry.get_asset_path(env)
    target_asset_path = os.path.join(env.config.paths.temp, "audio", audio_entry.name)

    # Ensure the necessary directory exists
    os.makedirs(os.path.dirname(target_asset_path), exist_ok=True)
    shutil.move(original_asset_path, target_asset_path)

    return AudioDownloadResult(manifest_entry=audio_entry, awb_path=target_asset_path)


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

    files_for_export: list[AudioDownloadResult] = []

    log("INFO", "Downloading audio assets...")

    # Download all audio first to ensure `acb` and `awb` files exist at the same time for later processing
    for result in concurrent_run(
            download_audio_to_temp, [[env, audio_entry] for audio_entry in audio_entries], env.config.paths.log,
            key_of_call=lambda _, entry: entry.name
    ).values():
        # Skips pending-process for non-awb files
        if not result.awb_path.endswith(".awb"):
            continue

        files_for_export.append(result)

    log("INFO", f"Found {len(files_for_export)} awb files to export.")

    for idx, result in enumerate(files_for_export, start=1):
        progress = idx / len(files_for_export)

        log("INFO", f"Exporting audio ({idx} / {len(files_for_export)} - {progress:.2%}) - {result.awb_path}")

        export_awb_subsongs(env, result)

    log_group_end()
