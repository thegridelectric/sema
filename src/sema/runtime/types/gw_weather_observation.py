from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import LowercaseToken
from sema.runtime.property_format import UtcIso8601Seconds
from sema.runtime.types.gw_weather_observation_reading import (
    GwWeatherObservationReading,
)


class GwWeatherObservation(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.observation/001"""

    station_alias: LowercaseToken
    observation_time: UtcIso8601Seconds
    interpolated: bool
    reading_list: list[GwWeatherObservationReading]
    type_name: Literal["gw.weather.observation"] = "gw.weather.observation"
    version: Literal["001"] = "001"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherObservation":
        """
        Axiom 1: NonEmptyReadings
        ReadingList SHALL be non-empty.
        """
        if len(self.reading_list) == 0:
            raise ValueError(
                "Axiom 1 (NonEmptyReadings) failed: ReadingList must be non-empty."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwWeatherObservation":
        """
        Axiom 2: DistinctChannels
        ChannelName SHALL be distinct across ReadingList.
        """
        names = [r.channel_name for r in self.reading_list]
        if len(set(names)) != len(names):
            raise ValueError(
                "Axiom 2 (DistinctChannels) failed: ChannelName must be distinct "
                f"across ReadingList; got {names!r}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_3(self) -> "GwWeatherObservation":
        """
        Axiom 3: DistinctQuantities
        Quantity SHALL be distinct across ReadingList.
        """
        quantities = [r.quantity for r in self.reading_list]
        if len(set(quantities)) != len(quantities):
            raise ValueError(
                "Axiom 3 (DistinctQuantities) failed: Quantity must be distinct "
                f"across ReadingList; got {[q.value for q in quantities]!r}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_4(self) -> "GwWeatherObservation":
        """
        Axiom 4: StationNaming
        Every ChannelName in ReadingList SHALL begin with StationAlias followed
        by ".".
        """
        prefix = f"{self.station_alias}."
        for reading in self.reading_list:
            if not reading.channel_name.startswith(prefix):
                raise ValueError(
                    "Axiom 4 (StationNaming) failed: ChannelName "
                    f"{reading.channel_name!r} must begin with {prefix!r}."
                )
        return self
