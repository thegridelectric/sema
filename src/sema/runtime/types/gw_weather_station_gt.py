from typing import Literal
from pydantic import StrictInt, model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import LowercaseToken
from sema.runtime.property_format import NonEmptyString
from sema.runtime.property_format import UUID4Str
from sema.runtime.property_format import UtcIso8601Seconds


class GwWeatherStationGt(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.station.gt/000"""

    alias: LowercaseToken
    display_name: NonEmptyString
    latitude_microdegrees: StrictInt
    longitude_microdegrees: StrictInt
    icao_id: NonEmptyString | None = None
    ghcn_id: NonEmptyString | None = None
    wunderground_id: NonEmptyString | None = None
    start: UtcIso8601Seconds
    id: UUID4Str
    type_name: Literal["gw.weather.station.gt"] = "gw.weather.station.gt"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherStationGt":
        """
        Axiom 1: CoordinateBounds
        a. The absolute value of LatitudeMicrodegrees SHALL be at most 90000000.
        b. The absolute value of LongitudeMicrodegrees SHALL be at most 180000000.
        """
        if abs(self.latitude_microdegrees) > 90_000_000:
            raise ValueError(
                "Axiom 1 (CoordinateBounds, clause a) failed: |LatitudeMicrodegrees| "
                f"must be at most 90000000; got {self.latitude_microdegrees}."
            )
        if abs(self.longitude_microdegrees) > 180_000_000:
            raise ValueError(
                "Axiom 1 (CoordinateBounds, clause b) failed: |LongitudeMicrodegrees| "
                f"must be at most 180000000; got {self.longitude_microdegrees}."
            )
        return self
