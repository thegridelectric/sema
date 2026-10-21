from enum import auto

from sema.runtime.enums.gw_str_enum import SemaEnum


class GwDashboardRole(SemaEnum):
    """Sema: https://schemas.electricity.works/enums/gw.dashboard.role/000"""

    Admin = auto()
    Owner = auto()
    Viewer = auto()

    @classmethod
    def default(cls) -> "GwDashboardRole":
        return cls.Viewer

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "gw.dashboard.role"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
