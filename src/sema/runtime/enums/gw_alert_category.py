from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwAlertCategory(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.alert.category/000"""

    Unknown = auto()
    House = auto()
    Fleet = auto()
    PlatformService = auto()

    @classmethod
    def default(cls) -> "GwAlertCategory":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.alert.category"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
