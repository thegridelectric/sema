from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class PicoResetCause(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/pico.reset.cause/000"""

    Unknown = auto()
    PowerOn = auto()
    Watchdog = auto()
    SelfReset = auto()

    @classmethod
    def default(cls) -> "PicoResetCause":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "pico.reset.cause"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
