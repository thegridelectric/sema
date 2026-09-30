from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwDispatchRefusalReason(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.dispatch.refusal.reason/000"""

    Standby = auto()
    NoAggregator = auto()
    ServiceContractBroken = auto()

    @classmethod
    def default(cls) -> "GwDispatchRefusalReason":
        return cls.Standby

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.dispatch.refusal.reason"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
