from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwAlertState(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.alert.state/000"""

    Firing = auto()
    Resolved = auto()

    @classmethod
    def default(cls) -> "GwAlertState":
        return cls.Firing

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.alert.state"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
