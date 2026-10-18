from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.types.gw_weather_forecast_channel_gt import GwWeatherForecastChannelGt
from sema.runtime.types.old_versions.gw_weather_channel_gt_000 import (
    GwWeatherChannelGt000,
)
from sema.runtime.types.old_versions.gw_weather_create_cmd_001 import (
    GwWeatherCreateCmd001,
)
from sema.runtime.types.old_versions.gw_weather_forecast_bundle_gt_000 import (
    GwWeatherForecastBundleGt000,
)
from sema.runtime.types.old_versions.gw_weather_location_gt_000 import (
    GwWeatherLocationGt000,
)


class GwWeatherCreateCmd000(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.create.cmd/000"""

    record: (
        GwWeatherChannelGt000
        | GwWeatherForecastBundleGt000
        | GwWeatherForecastChannelGt
        | GwWeatherLocationGt000
    )
    proof: str | None = None
    type_name: Literal["gw.weather.create.cmd"] = "gw.weather.create.cmd"
    version: Literal["000"] = "000"

    def upgrade(self) -> GwWeatherCreateCmd001:
        """
        - Record: oneOf gains gw.weather.seasonal.template.gt/000
        - Record: gw.weather.channel.gt and gw.weather.forecast.bundle.gt at 001
        """
        data = self.model_dump()
        data["version"] = "001"
        return GwWeatherCreateCmd001.model_validate(data)
