from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.types.gw_weather_channel_gt import GwWeatherChannelGt
from sema.runtime.types.gw_weather_forecast_bundle_gt import GwWeatherForecastBundleGt
from sema.runtime.types.gw_weather_forecast_channel_gt import GwWeatherForecastChannelGt
from sema.runtime.types.gw_weather_location_gt import GwWeatherLocationGt
from sema.runtime.types.gw_weather_seasonal_template_gt import (
    GwWeatherSeasonalTemplateGt,
)
from sema.runtime.types.gw_weather_station_gt import GwWeatherStationGt


class GwWeatherCreateCmd(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.create.cmd/002"""

    record: (
        GwWeatherChannelGt
        | GwWeatherForecastBundleGt
        | GwWeatherForecastChannelGt
        | GwWeatherLocationGt
        | GwWeatherSeasonalTemplateGt
        | GwWeatherStationGt
    )
    proof: str | None = None
    type_name: Literal["gw.weather.create.cmd"] = "gw.weather.create.cmd"
    version: Literal["002"] = "002"
