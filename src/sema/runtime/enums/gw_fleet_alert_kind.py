from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwFleetAlertKind(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.fleet.alert.kind/000"""

    Unknown = auto()
    AllHousesSilent = auto()

    @classmethod
    def default(cls) -> "GwFleetAlertKind":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.fleet.alert.kind"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
