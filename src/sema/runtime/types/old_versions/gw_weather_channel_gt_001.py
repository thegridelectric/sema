from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1Quantity
from sema.runtime.enums import Gw1Unit
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import NonEmptyString
from sema.runtime.property_format import NonNegativeInt
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import UUID4Str
from sema.runtime.property_format import UtcIso8601Seconds
from sema.runtime.types.gw_weather_channel_gt import GwWeatherChannelGt


class GwWeatherChannelGt001(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.channel.gt/001"""

    name: LeftRightDot
    display_name: NonEmptyString
    quantity: Gw1Quantity
    unit: Gw1Unit
    location_alias: LeftRightDot
    emit_period_s: PositiveInt
    emit_offset_s: NonNegativeInt
    start: UtcIso8601Seconds
    id: UUID4Str
    type_name: Literal["gw.weather.channel.gt"] = "gw.weather.channel.gt"
    version: Literal["001"] = "001"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwWeatherChannelGt001":
        """
        Axiom 1: NameDerivation
        Name SHALL equal LocationAlias + "." + the lowercased Quantity value, optionally
        followed by "." and one or more further segments (a variant suffix for a
        semantically different series, never acquisition detail).
        """
        derived = f"{self.location_alias}.{self.quantity.value.lower()}"
        if not (self.name == derived or self.name.startswith(derived + ".")):
            raise ValueError(
                "Axiom 1 (NameDerivation) failed: Name must equal "
                f"LocationAlias + '.' + lowercased Quantity ('{derived}'), "
                f"optionally followed by a variant suffix; got '{self.name}'."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwWeatherChannelGt001":
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

    def upgrade(self) -> GwWeatherChannelGt:
        """
        - LocationAlias: removed; StationAlias: add (the gw.weather.station.gt whose readings this series is)
        - Name: derived from StationAlias and Quantity
        """
        raise SemaType.upgrade_requires_context(
            "GwWeatherChannelGt001 cannot be upgraded to "
            "GwWeatherChannelGt without context: v002 names "
            "the station whose readings the series is, which the old record does "
            "not say and SHALL NOT be guessed."
        )
