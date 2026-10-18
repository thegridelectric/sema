from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.types.gw_weather_create_cmd import GwWeatherCreateCmd
from sema.runtime.types.gw_weather_forecast_channel_gt import GwWeatherForecastChannelGt
from sema.runtime.types.gw_weather_seasonal_template_gt import (
    GwWeatherSeasonalTemplateGt,
)
from sema.runtime.types.old_versions.gw_weather_channel_gt_001 import (
    GwWeatherChannelGt001,
)
from sema.runtime.types.old_versions.gw_weather_forecast_bundle_gt_001 import (
    GwWeatherForecastBundleGt001,
)
from sema.runtime.types.old_versions.gw_weather_location_gt_000 import (
    GwWeatherLocationGt000,
)


class GwWeatherCreateCmd001(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.create.cmd/001"""

    record: (
        GwWeatherChannelGt001
        | GwWeatherForecastBundleGt001
        | GwWeatherForecastChannelGt
        | GwWeatherLocationGt000
        | GwWeatherSeasonalTemplateGt
    )
    proof: str | None = None
    type_name: Literal["gw.weather.create.cmd"] = "gw.weather.create.cmd"
    version: Literal["001"] = "001"

    def upgrade(self) -> GwWeatherCreateCmd:
        """
        - Record: gw.weather.forecast.bundle.gt 001 -> 002
        - Record: gw.weather.channel.gt 001 -> 002
        - Record: gw.weather.location.gt 000 -> 001
        - Record: oneOf gains gw.weather.station.gt/000
        """
        data = self.model_dump()
        if isinstance(
            self.record,
            GwWeatherForecastBundleGt001
            | GwWeatherChannelGt001
            | GwWeatherLocationGt000,
        ):
            data["record"] = self.record.upgrade()
        data["version"] = "002"
        return GwWeatherCreateCmd.model_validate(data)
