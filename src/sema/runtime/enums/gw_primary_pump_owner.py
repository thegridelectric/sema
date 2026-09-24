from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwPrimaryPumpOwner(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.primary.pump.owner/000"""

    HeatPump = auto()
    Scada = auto()

    @classmethod
    def default(cls) -> "GwPrimaryPumpOwner":
        return cls.HeatPump

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.primary.pump.owner"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
