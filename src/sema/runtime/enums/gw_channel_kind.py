from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwChannelKind(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.channel.kind/000"""

    Unknown = auto()
    DataChannel = auto()
    DerivedChannel = auto()
    SynthChannel = auto()
    StateMachine = auto()
    HeatCallSynth = auto()
    WeatherForecast = auto()
    FloParams = auto()

    @classmethod
    def default(cls) -> "GwChannelKind":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.channel.kind"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
