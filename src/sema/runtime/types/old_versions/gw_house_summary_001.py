from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import GwDashboardRole
from sema.runtime.property_format import GitCommit
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import SpaceheatName
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.property_format import UUID4Str
from sema.runtime.property_format import UtcIso8601Seconds
from sema.runtime.types.gw_house_operating_status import GwHouseOperatingStatus
from sema.runtime.types.old_versions.gw_house_summary_002 import GwHouseSummary002
from sema.runtime.types.old_versions.layout_lite_011 import LayoutLite011
from sema.runtime.types.old_versions.layout_lite_012 import LayoutLite012
from sema.runtime.types.old_versions.layout_lite_013 import LayoutLite013


class GwHouseSummary001(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.house.summary/001"""

    role: GwDashboardRole
    ta_g_node_id: UUID4Str
    g_node_alias: LeftRightDot
    display_name: str | None = None
    layout: LayoutLite011 | LayoutLite012 | LayoutLite013 | None = None
    operating_status: GwHouseOperatingStatus | None = None
    latest_snapshot_time: UtcIso8601Seconds | None = None
    longest_running_zone_name: SpaceheatName | None = None
    longest_running_zone_start_time: UtcIso8601Seconds | None = None
    scada_commit: GitCommit | None = None
    send_time_ms: UTCMilliseconds
    type_name: Literal["gw.house.summary"] = "gw.house.summary"
    version: Literal["001"] = "001"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwHouseSummary001":
        """
        Axiom 1: ZonePairTogether
        LongestRunningZoneName and LongestRunningZoneStartTime SHALL be present
        together or absent together.
        """
        if (self.longest_running_zone_name is None) != (
            self.longest_running_zone_start_time is None
        ):
            raise ValueError(
                "Axiom 1 (ZonePairTogether) failed: LongestRunningZoneName and "
                "LongestRunningZoneStartTime are present together or absent together."
            )
        return self

    def upgrade(self) -> GwHouseSummary002:
        """
        Adds optional ScadaCommitStanding (gw.commit.standing): where ScadaCommit stands against the scada repository's main head, derived by the backend; axiom 2: absent when ScadaCommit is absent.
        """
        data = self.model_dump()
        data["version"] = "002"
        return GwHouseSummary002.model_validate(data)
