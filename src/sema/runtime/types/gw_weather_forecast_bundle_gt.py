from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import NonEmptyString
from sema.runtime.property_format import NonNegativeInt
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import UUID4Str
from sema.runtime.property_format import UtcIso8601Seconds
from sema.runtime.types.gw_weather_channel_gt import GwWeatherChannelGt
from sema.runtime.types.gw_weather_forecast_channel_gt import GwWeatherForecastChannelGt


class GwWeatherForecastBundleGt(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.forecast.bundle.gt/002"""

    name: LeftRightDot
    display_name: NonEmptyString
    location_alias: LeftRightDot
    temp_forecast_channel: GwWeatherForecastChannelGt
    temp_observation_channel: GwWeatherChannelGt
    wind_speed_forecast_channel: GwWeatherForecastChannelGt
    wind_speed_observation_channel: GwWeatherChannelGt
    irradiance_forecast_channel: GwWeatherForecastChannelGt
    irradiance_observation_channel: GwWeatherChannelGt
    emit_period_s: PositiveInt
    emit_offset_s: NonNegativeInt
    start: UtcIso8601Seconds
    id: UUID4Str
    type_name: Literal["gw.weather.forecast.bundle.gt"] = (
        "gw.weather.forecast.bundle.gt"
    )
    version: Literal["002"] = "002"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherForecastBundleGt":
        """
        Axiom 1: SharedSliceGrid
        TempForecastChannel, WindSpeedForecastChannel and
        IrradianceForecastChannel SHALL declare identical SliceDurationSList.
        """
        grid = self.temp_forecast_channel.slice_duration_s_list
        if (
            self.wind_speed_forecast_channel.slice_duration_s_list != grid
            or self.irradiance_forecast_channel.slice_duration_s_list != grid
        ):
            raise ValueError(
                "Axiom 1 (SharedSliceGrid) failed: TempForecastChannel, "
                "WindSpeedForecastChannel and IrradianceForecastChannel must "
                "declare identical SliceDurationSList."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwWeatherForecastBundleGt":
        """
        Axiom 2: EmitOffsetBound
        EmitOffsetS SHALL be strictly less than EmitPeriodS.
        """
        if not self.emit_offset_s < self.emit_period_s:
            raise ValueError(
                "Axiom 2 (EmitOffsetBound) failed: EmitOffsetS "
                f"({self.emit_offset_s}) must be strictly less than "
                f"EmitPeriodS ({self.emit_period_s})."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_3(self) -> "GwWeatherForecastBundleGt":
        """
        Axiom 3: DistinctChannels
        TempForecastChannel.Name, WindSpeedForecastChannel.Name and
        IrradianceForecastChannel.Name SHALL be pairwise distinct.
        """
        names = (
            self.temp_forecast_channel.name,
            self.wind_speed_forecast_channel.name,
            self.irradiance_forecast_channel.name,
        )
        if len(set(names)) != len(names):
            raise ValueError(
                "Axiom 3 (DistinctChannels) failed: the three forecast "
                f"channel Names must be pairwise distinct; got {names!r}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_4(self) -> "GwWeatherForecastBundleGt":
        """
        Axiom 4: TargetBinding
        TempForecastChannel.TargetChannelName SHALL equal
        TempObservationChannel.Name, WindSpeedForecastChannel.TargetChannelName
        SHALL equal WindSpeedObservationChannel.Name, and
        IrradianceForecastChannel.TargetChannelName SHALL equal
        IrradianceObservationChannel.Name.
        """
        if (
            self.temp_forecast_channel.target_channel_name
            != self.temp_observation_channel.name
            or self.wind_speed_forecast_channel.target_channel_name
            != self.wind_speed_observation_channel.name
            or self.irradiance_forecast_channel.target_channel_name
            != self.irradiance_observation_channel.name
        ):
            raise ValueError(
                "Axiom 4 (TargetBinding) failed: each forecast channel's "
                "TargetChannelName must equal its paired observation "
                "channel's Name."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_5(self) -> "GwWeatherForecastBundleGt":
        """
        Axiom 5: QuantityTargeting
        TempObservationChannel.Quantity SHALL be Temperature,
        WindSpeedObservationChannel.Quantity SHALL be WindSpeed, and
        IrradianceObservationChannel.Quantity SHALL be Irradiance.
        """
        got = (
            self.temp_observation_channel.quantity.value,
            self.wind_speed_observation_channel.quantity.value,
            self.irradiance_observation_channel.quantity.value,
        )
        if got != ("Temperature", "WindSpeed", "Irradiance"):
            raise ValueError(
                "Axiom 5 (QuantityTargeting) failed: the observation channels "
                "must have Quantity Temperature, WindSpeed and Irradiance in "
                f"that order; got {got!r}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_6(self) -> "GwWeatherForecastBundleGt":
        """
        Axiom 6: LocationConsistency
        TempObservationChannel.LocationAlias,
        WindSpeedObservationChannel.LocationAlias and
        IrradianceObservationChannel.LocationAlias SHALL equal LocationAlias.
        """
        if (
            self.temp_observation_channel.location_alias != self.location_alias
            or self.wind_speed_observation_channel.location_alias != self.location_alias
            or self.irradiance_observation_channel.location_alias != self.location_alias
        ):
            raise ValueError(
                "Axiom 6 (LocationConsistency) failed: every observation "
                "channel's LocationAlias must equal "
                f"{self.location_alias!r}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_7(self) -> "GwWeatherForecastBundleGt":
        """
        Axiom 7: ForecastNaming
        Name SHALL equal LocationAlias + ".forecast." followed by one or more
        further segments.
        """
        prefix = f"{self.location_alias}.forecast."
        if not (self.name.startswith(prefix) and len(self.name) > len(prefix)):
            raise ValueError(
                f"Axiom 7 (ForecastNaming) failed: {self.name!r} must equal "
                f"{prefix!r} followed by one or more further segments."
            )
        return self
