from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import GwAlertCategory
from sema.runtime.enums import GwAlertState
from sema.runtime.enums import GwFleetAlertKind
from sema.runtime.enums import GwHouseAlertKind
from sema.runtime.enums import GwPlatformAlertKind
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.property_format import UUID4Str
from sema.runtime.types.channel_readings import ChannelReadings


class GwAlert(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.alert/000"""

    src: LeftRightDot
    category: GwAlertCategory
    kind: GwHouseAlertKind | GwFleetAlertKind | GwPlatformAlertKind
    state: GwAlertState
    alert_id: UUID4Str
    about_g_node_alias: LeftRightDot | None = None
    subject: str | None = None
    raised_ms: UTCMilliseconds
    resolved_ms: UTCMilliseconds | None = None
    summary: str
    evidence: list[ChannelReadings] | None = None
    type_name: Literal["gw.alert"] = "gw.alert"
    version: Literal["000"] = "000"

    @staticmethod
    def kind_enum_for(
        category: GwAlertCategory,
    ) -> (
        type[GwHouseAlertKind]
        | type[GwFleetAlertKind]
        | type[GwPlatformAlertKind]
        | None
    ):
        """The kind enum a Category selects; None for a category this
        version does not know."""
        return {
            GwAlertCategory.House: GwHouseAlertKind,
            GwAlertCategory.Fleet: GwFleetAlertKind,
            GwAlertCategory.PlatformService: GwPlatformAlertKind,
        }.get(category)

    @model_validator(mode="before")
    @classmethod
    def decode_kind_by_category(cls, data: object) -> object:
        """
        Decode Kind with the enum Category selects (axiom 1). The runtime's
        string enums fall back to their default on an unknown value, so a
        union of kind enums would let the first branch swallow every value;
        dispatching on Category keeps a Fleet or PlatformService kind in its
        own enum and keeps the newer-version fallback to Unknown.
        """
        if not isinstance(data, dict):
            return data
        category_key = "Category" if "Category" in data else "category"
        kind_key = "Kind" if "Kind" in data else "kind"
        if category_key not in data or kind_key not in data:
            return data
        kind_enum = cls.kind_enum_for(GwAlertCategory(str(data[category_key])))
        if kind_enum is None:
            return data
        value = str(data[kind_key])
        elsewhere = {
            v
            for other in (GwHouseAlertKind, GwFleetAlertKind, GwPlatformAlertKind)
            if other is not kind_enum
            for v in other.values()
        }
        if value not in kind_enum.values() and value in elsewhere:
            raise ValueError(
                f"CategoryKindConsistency: Category {data[category_key]} requires a Kind "
                f"from {kind_enum.__name__}; got {value!r}."
            )
        return {**data, kind_key: kind_enum(value)}

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwAlert":
        """
        Axiom 1: CategoryKindConsistency
        Category SHALL determine the enum Kind belongs to: a. If Category is House, Kind
        SHALL be a value of gw.house.alert.kind. b. If Category is Fleet, Kind SHALL be a
        value of gw.fleet.alert.kind. c. If Category is PlatformService, Kind SHALL be a
        value of gw.platform.alert.kind.
        """
        kind_enum = self.kind_enum_for(self.category)
        if kind_enum is not None and not isinstance(self.kind, kind_enum):
            raise ValueError(
                f"CategoryKindConsistency: Category {self.category.value} requires a Kind "
                f"from {kind_enum.__name__}; got {type(self.kind).__name__}.{self.kind.value}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwAlert":
        """
        Axiom 2: HouseSubject
        a. If Category is House, AboutGNodeAlias SHALL be present. b. If AboutGNodeAlias is
        present, it SHALL identify a TerminalAsset and therefore SHALL end with the suffix
        ".ta".
        """
        if self.category == GwAlertCategory.House and self.about_g_node_alias is None:
            raise ValueError("HouseSubject: Category House requires AboutGNodeAlias.")
        if self.about_g_node_alias is not None and not self.about_g_node_alias.endswith(
            ".ta"
        ):
            raise ValueError(
                f'HouseSubject: AboutGNodeAlias ({self.about_g_node_alias}) does not end with the suffix ".ta".'
            )
        return self

    @model_validator(mode="after")
    def check_axiom_3(self) -> "GwAlert":
        """
        Axiom 3: ResolvedTime
        a. If State is Resolved, ResolvedMs SHALL be present. b. If State is Firing,
        ResolvedMs SHALL be absent.
        """
        if self.state == GwAlertState.Resolved and self.resolved_ms is None:
            raise ValueError("ResolvedTime: State Resolved requires ResolvedMs.")
        if self.state == GwAlertState.Firing and self.resolved_ms is not None:
            raise ValueError("ResolvedTime: State Firing forbids ResolvedMs.")
        return self
