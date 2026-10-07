from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwExperimentVerdict(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.experiment.verdict/000"""

    Unknown = auto()
    Pass = auto()
    Fail = auto()
    Inconclusive = auto()

    @classmethod
    def default(cls) -> "GwExperimentVerdict":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.experiment.verdict"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
