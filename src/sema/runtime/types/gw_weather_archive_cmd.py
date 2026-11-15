from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import LowercaseToken
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.property_format import UtcIso8601Seconds


class GwWeatherArchiveCmd(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.archive.cmd/000"""

    station_alias: LowercaseToken
    channel_name_list: list[LeftRightDot]
    method: LeftRightDot
    source_locator: str
    start: UtcIso8601Seconds
    end: UtcIso8601Seconds
    created_ms: UTCMilliseconds
    proof: str | None = None
    type_name: Literal["gw.weather.archive.cmd"] = "gw.weather.archive.cmd"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherArchiveCmd":
        """
        Axiom 1: WindowOrder
        End SHALL be later than Start.
        """
        if self.end <= self.start:
            raise ValueError(
                "Axiom 1 (WindowOrder) failed: End must be later than Start; "
                f"got Start={self.start}, End={self.end}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwWeatherArchiveCmd":
        """
        Axiom 2: StationNaming
        Every element of ChannelNameList SHALL begin with StationAlias followed by ".".
        """
        prefix = f"{self.station_alias}."
        for name in self.channel_name_list:
            if not name.startswith(prefix):
                raise ValueError(
                    "Axiom 2 (StationNaming) failed: every ChannelNameList element "
                    f"must begin with {prefix!r}; got {name!r}."
                )
        return self

    @model_validator(mode="after")
    def check_axiom_3(self) -> "GwWeatherArchiveCmd":
        """
        Axiom 3: DistinctChannels
        Elements of ChannelNameList SHALL be distinct.
        """
        if len(set(self.channel_name_list)) != len(self.channel_name_list):
            raise ValueError(
                "Axiom 3 (DistinctChannels) failed: ChannelNameList elements must be "
                f"distinct; got {self.channel_name_list}."
            )
        return self
