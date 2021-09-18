"""Various environmental constants."""
from dlasset.enums import Locale

__all__ = ("CDN_BASE_URL", "MANIFEST_NAMES")

CDN_BASE_URL = "https://dragalialost.akamaized.net/dl"

MANIFEST_NAMES: dict[Locale, str] = {
    Locale.JP: "assetbundle.manifest",
    Locale.EN: "assetbundle.en_us.manifest",
    Locale.CHS: "assetbundle.zh_cn.manifest",
    Locale.CHT: "assetbundle.zh_tw.manifest",
}
