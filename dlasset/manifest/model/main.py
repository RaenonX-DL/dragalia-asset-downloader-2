"""Manifest model class."""
import re
from dataclasses import dataclass, field
from typing import Callable, Generator, Iterable, Pattern, TypeVar, cast

from dlasset.enums import Locale
from dlasset.export import MonoBehaviourTree
from .entry import ManifestEntry, ManifestEntryBase, ManifestRawEntry
from .locale import ManifestLocale

__all__ = ("Manifest",)

T = TypeVar("T", bound=ManifestEntryBase)


@dataclass
class Manifest:
    """Manifest of all locales."""

    data: dict[Locale, MonoBehaviourTree]

    manifests: dict[Locale, ManifestLocale] = field(init=False)

    def __post_init__(self) -> None:
        self.manifests = {locale: ManifestLocale(manifest) for locale, manifest in self.data.items()}

    def get_entries_including_dependencies(
            self, locale: Locale, parent_entry: T
    ) -> list[T]:
        """Get ``parent_entry`` and its dependencies attached at the tail of the returned entry list."""
        ret = [parent_entry]
        for dependency in parent_entry.dependencies:
            dependency_entry = self.manifests[locale].entry_by_name[dependency]
            ret.extend(self.get_entries_including_dependencies(locale, cast(T, dependency_entry)))
        return ret

    def get_manifest_entries_of_locale(
            self, regex: Pattern, get_entries: Callable[[ManifestLocale], Iterable[T]], *,
            is_master_only: bool
    ) -> Generator[tuple[Locale, list[T]], None, None]:
        """
        Get a generator yielding locale and the entry with its name matching ``regex`` from ``entries``.

        Yields the manifest in the master locale only if ``is_master_only`` is ``True``.

        Resolves asset dependecy.
        """
        for locale, manifest_of_locale in self.manifests.items():
            if is_master_only and not locale.is_master:
                continue

            for entry in get_entries(manifest_of_locale):
                if not re.match(regex, entry.name):
                    continue

                yield locale, self.get_entries_including_dependencies(locale, entry)

    def get_entry_with_regex(
            self, regex: Pattern, *,
            is_master_only: bool
    ) -> Generator[tuple[Locale, list[ManifestEntry]], None, None]:
        """
        Get a generator yielding the manifest entry with its name matching ``regex``.

        Resolves asset dependecy.
        """
        return self.get_manifest_entries_of_locale(
            regex, lambda manifest: manifest.entries_across_category,
            is_master_only=is_master_only
        )

    def get_raw_entry_with_regex(
            self, regex: Pattern, *,
            is_master_only: bool
    ) -> Generator[tuple[Locale, list[ManifestRawEntry]], None, None]:
        """
        Get a generator yielding the manifest entry with its name matching ``regex``.

        Resolves asset dependecy.
        """
        return self.get_manifest_entries_of_locale(
            regex, lambda manifest: manifest.raw_assets,
            is_master_only=is_master_only
        )
