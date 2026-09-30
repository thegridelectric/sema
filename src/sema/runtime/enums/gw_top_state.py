from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwTopState(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.top.state/000"""

    Auto = auto()
    Admin = auto()

    @classmethod
    def default(cls) -> "GwTopState":
        return cls.Auto

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.top.state"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
