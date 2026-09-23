from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class ZoneEmitterType(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/zone.emitter.type/000"""

    Unknown = auto()
    FinTube = auto()
    CastIronBaseboard = auto()
    CastIronRadiator = auto()
    FanCoil = auto()
    RadiantSlab = auto()
    StoreUnderFloor = auto()

    @classmethod
    def default(cls) -> "ZoneEmitterType":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "zone.emitter.type"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
