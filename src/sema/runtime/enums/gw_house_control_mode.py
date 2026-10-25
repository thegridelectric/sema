from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwHouseControlMode(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.house.control.mode/000"""

    Unknown = auto()
    LocalControl = auto()
    Ltn = auto()
    Admin = auto()

    @classmethod
    def default(cls) -> "GwHouseControlMode":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.house.control.mode"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
