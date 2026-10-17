from typing import Literal
from pydantic import StrictInt, model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1Quantity
from sema.runtime.enums import GwWeatherForecastFidelity
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UtcIso8601Seconds


class GwWeatherForecastSeries(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.forecast.series/000"""

    channel_name: LeftRightDot
    quantity: Gw1Quantity
    values: list[StrictInt]
    fidelity: GwWeatherForecastFidelity
    source_updated_time: UtcIso8601Seconds
    type_name: Literal["gw.weather.forecast.series"] = "gw.weather.forecast.series"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherForecastSeries":
        """
        Axiom 1: NonEmptyValues
        Values SHALL be non-empty.
        """
        if len(self.values) == 0:
            raise ValueError(
                "Axiom 1 (NonEmptyValues) failed: Values must be non-empty."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwWeatherForecastSeries":
        """
        Axiom 2: ForecastNaming
        ChannelName SHALL contain "forecast" as an interior segment.
        """
        if "forecast" not in self.channel_name.split(".")[1:-1]:
            raise ValueError(
                "Axiom 2 (ForecastNaming) failed: ChannelName "
                f"{self.channel_name!r} must contain 'forecast' as an interior "
                "segment."
            )
        return self
