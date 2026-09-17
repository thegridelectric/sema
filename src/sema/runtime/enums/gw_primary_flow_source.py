from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwPrimaryFlowSource(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.primary.flow.source/000"""

    Measured = auto()
    DerivedSiegSum = auto()

    @classmethod
    def default(cls) -> "GwPrimaryFlowSource":
        return cls.Measured

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.primary.flow.source"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
