from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwPlatformAlertKind(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.platform.alert.kind/000"""

    Unknown = auto()
    BrokerUnreachable = auto()

    @classmethod
    def default(cls) -> "GwPlatformAlertKind":
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.platform.alert.kind"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
