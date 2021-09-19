"""Manifest model class."""
import re
from dataclasses import dataclass, field
from typing import Generator, Pattern

from dlasset.enums import Locale
from dlasset.export import MonoBehaviourTree
from .entry import ManifestEntry
from .locale import ManifestLocale

__all__ = ("Manifest",)


@dataclass
class Manifest:
    """Manifest of all locales."""

    data: dict[Locale, MonoBehaviourTree]

    manifests: dict[Locale, ManifestLocale] = field(init=False)

    def __post_init__(self) -> None:
        self.manifests = {locale: ManifestLocale(manifest) for locale, manifest in self.data.items()}

    def get_entry_with_regex(
            self, regex: Pattern, *,
            is_master_only: bool
    ) -> Generator[tuple[Locale, ManifestEntry], None, None]:
        """Get the generator yielding the manifest entry with its name matching ``regex``."""
        for locale, manifest_of_locale in self.manifests.items():
            if is_master_only and not locale.is_master:
                continue

            for entry in manifest_of_locale.entries_across_category:
                if not re.match(regex, entry.name):
                    continue

                yield locale, entry
