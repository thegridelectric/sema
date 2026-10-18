from typing import Literal
from pydantic import StrictInt, model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import NonEmptyString
from sema.runtime.property_format import UUID4Str
from sema.runtime.types.gw_weather_location_gt import GwWeatherLocationGt


class GwWeatherLocationGt000(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.location.gt/000"""

    alias: LeftRightDot
    latitude_microdegrees: StrictInt
    longitude_microdegrees: StrictInt
    timezone: NonEmptyString
    icao_id: NonEmptyString | None = None
    wban_id: NonEmptyString | None = None
    ghcn_id: NonEmptyString | None = None
    coop_id: NonEmptyString | None = None
    id: UUID4Str
    type_name: Literal["gw.weather.location.gt"] = "gw.weather.location.gt"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherLocationGt000":
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

    def upgrade(self) -> GwWeatherLocationGt:
        """
        - IcaoId, WbanId, GhcnId, CoopId: removed (station identifiers live on gw.weather.station.gt)
        - Timezone: iana.timezone.str
        """
        data = self.model_dump()
        for field in ("icao_id", "wban_id", "ghcn_id", "coop_id"):
            data.pop(field, None)
        data["version"] = "001"
        return GwWeatherLocationGt.model_validate(data)
