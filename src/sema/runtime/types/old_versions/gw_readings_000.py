from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.types.channel_readings import ChannelReadings
from sema.runtime.types.gw_readings import GwReadings
from sema.runtime.types.old_versions.data_channel_gt_003 import DataChannelGt003
from sema.runtime.types.old_versions.derived_channel_gt_002 import DerivedChannelGt002


class GwReadings000(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.readings/000"""

    ta_alias: LeftRightDot
    start_unix_ms: UTCMilliseconds
    end_unix_ms: UTCMilliseconds
    channels: list[DataChannelGt003 | DerivedChannelGt002]
    channel_readings_list: list[ChannelReadings]
    type_name: Literal["gw.readings"] = "gw.readings"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwReadings000":
        """
        Axiom 1: WindowOrder
        EndUnixMs SHALL be greater than StartUnixMs.
        """
        if not self.end_unix_ms > self.start_unix_ms:
            raise ValueError(
                "Axiom 1 (WindowOrder) failed: EndUnixMs must be greater "
                "than StartUnixMs."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwReadings000":
        """
        Axiom 2: ReadingsChannelCoverage
        Each ChannelReadingsList entry's ChannelName SHALL equal the Name
        of exactly one entry in Channels.
        """
        channel_names = [c.name for c in self.channels]
        for cr in self.channel_readings_list:
            if channel_names.count(cr.channel_name) != 1:
                raise ValueError(
                    "Axiom 2 (ReadingsChannelCoverage) failed: "
                    f"ChannelReadingsList entry {cr.channel_name!r} must "
                    "match exactly one Channels entry by Name."
                )
        return self

    def upgrade(self) -> GwReadings:
        """
        - Channels[]: data.channel.gt 003 -> 004
        - Channels[]: derived.channel.gt 002 -> 003
        """
        data = self.model_dump()
        data["channels"] = [c.upgrade().model_dump() for c in self.channels]
        data["version"] = "001"
        return GwReadings.model_validate(data)
