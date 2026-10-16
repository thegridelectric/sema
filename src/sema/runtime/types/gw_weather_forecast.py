from typing import Literal
from pydantic import StrictInt, model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import GwWeatherForecastFidelity
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.property_format import UtcIso8601Seconds


class GwWeatherForecast(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.forecast/001"""

    bundle_name: LeftRightDot
    source_updated_time: UtcIso8601Seconds
    irradiance_source_updated_time: UtcIso8601Seconds
    message_created_ms: UTCMilliseconds
    first_slice_start: UtcIso8601Seconds
    temp_channel_name: LeftRightDot
    temp_values: list[StrictInt]
    temp_fidelity: GwWeatherForecastFidelity
    wind_speed_channel_name: LeftRightDot
    wind_speed_values: list[StrictInt]
    wind_speed_fidelity: GwWeatherForecastFidelity
    irradiance_channel_name: LeftRightDot
    irradiance_values: list[StrictInt]
    irradiance_fidelity: GwWeatherForecastFidelity
    type_name: Literal["gw.weather.forecast"] = "gw.weather.forecast"
    version: Literal["001"] = "001"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherForecast":
        """
        Axiom 1: NonEmptyValues
        TempValues, WindSpeedValues and IrradianceValues SHALL be non-empty.
        """
        if (
            len(self.temp_values) == 0
            or len(self.wind_speed_values) == 0
            or len(self.irradiance_values) == 0
        ):
            raise ValueError(
                "Axiom 1 (NonEmptyValues) failed: TempValues, WindSpeedValues "
                "and IrradianceValues must be non-empty."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwWeatherForecast":
        """
        Axiom 2: EqualValueLengths
        len(TempValues), len(WindSpeedValues) and len(IrradianceValues) SHALL be
        equal.
        """
        if not (
            len(self.temp_values)
            == len(self.wind_speed_values)
            == len(self.irradiance_values)
        ):
            raise ValueError(
                "Axiom 2 (EqualValueLengths) failed: "
                f"len(TempValues)={len(self.temp_values)}, "
                f"len(WindSpeedValues)={len(self.wind_speed_values)} and "
                f"len(IrradianceValues)={len(self.irradiance_values)} must be equal."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_3(self) -> "GwWeatherForecast":
        """
        Axiom 3: DistinctChannels
        TempChannelName, WindSpeedChannelName and IrradianceChannelName SHALL be
        pairwise distinct.
        """
        names = (
            self.temp_channel_name,
            self.wind_speed_channel_name,
            self.irradiance_channel_name,
        )
        if len(set(names)) != len(names):
            raise ValueError(
                "Axiom 3 (DistinctChannels) failed: TempChannelName, "
                "WindSpeedChannelName and IrradianceChannelName must be pairwise "
                f"distinct; got {names!r}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_4(self) -> "GwWeatherForecast":
        """
        Axiom 4: ForecastNaming
        a. BundleName SHALL contain "forecast" as an interior segment.
        b. TempChannelName SHALL contain "forecast" as an interior segment.
        c. WindSpeedChannelName SHALL contain "forecast" as an interior segment.
        d. IrradianceChannelName SHALL contain "forecast" as an interior segment.
        """
        for label, value in (
            ("a", self.bundle_name),
            ("b", self.temp_channel_name),
            ("c", self.wind_speed_channel_name),
            ("d", self.irradiance_channel_name),
        ):
            if "forecast" not in value.split(".")[1:-1]:
                raise ValueError(
                    f"Axiom 4 (ForecastNaming, clause {label}) failed: "
                    f"{value!r} must contain 'forecast' as an interior "
                    "segment."
                )
        return self
