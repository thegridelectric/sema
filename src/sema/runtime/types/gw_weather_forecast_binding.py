from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.types.gw_weather_channel_gt import GwWeatherChannelGt
from sema.runtime.types.gw_weather_forecast_channel_gt import GwWeatherForecastChannelGt


class GwWeatherForecastBinding(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.forecast.binding/000"""

    forecast_channel: GwWeatherForecastChannelGt
    observation_channel: GwWeatherChannelGt
    type_name: Literal["gw.weather.forecast.binding"] = "gw.weather.forecast.binding"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherForecastBinding":
        """
        Axiom 1: TargetBinding
        ForecastChannel.TargetChannelName SHALL equal ObservationChannel.Name.
        """
        if self.forecast_channel.target_channel_name != self.observation_channel.name:
            raise ValueError(
                "Axiom 1 (TargetBinding) failed: ForecastChannel.TargetChannelName "
                f"({self.forecast_channel.target_channel_name!r}) must equal "
                f"ObservationChannel.Name ({self.observation_channel.name!r})."
            )
        return self
