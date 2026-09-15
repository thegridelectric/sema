from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwHouseAlertKind(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.house.alert.kind/000"""

    Unknown = auto()
    NoData = auto()
    ScadaRebootLoop = auto()
    CriticalGlitch = auto()
    ZoneBelowSetpoint = auto()
    ZoneFreezeRisk = auto()
    NoDistFlow = auto()
    NoStoreFlow = auto()
    HpNotResponding = auto()
    HpRunningOnpeak = auto()
    LocalControlActive = auto()

    @classmethod
    def default(cls) -> "GwHouseAlertKind":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.house.alert.kind"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
