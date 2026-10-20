from typing import Literal
from pydantic import StrictFloat, model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCSeconds
from sema.runtime.property_format import UUID4Str


class GwStopgapPriceForecast(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.stopgap.price.forecast/000"""

    from_g_node_alias: LeftRightDot
    p_node_alias: LeftRightDot
    tariff_alias: LeftRightDot
    hour_start_s: list[UTCSeconds]
    lmp_list: list[StrictFloat]
    dist_list: list[StrictFloat]
    price_uid: UUID4Str
    forecast_created_s: UTCSeconds
    type_name: Literal["gw.stopgap.price.forecast"] = "gw.stopgap.price.forecast"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwStopgapPriceForecast":
        """
        Axiom 1: ListLengthConsistency
        HourStartS, LmpList and DistList SHALL all have the same length.
        """
        if len({len(self.hour_start_s), len(self.lmp_list), len(self.dist_list)}) > 1:
            raise ValueError(
                "Axiom 1 failed: hour_start_s, lmp_list and dist_list must all have the same length."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwStopgapPriceForecast":
        """
        Axiom 2: HoursAscending
        HourStartS SHALL be strictly increasing.
        """
        if any(b <= a for a, b in zip(self.hour_start_s, self.hour_start_s[1:])):
            raise ValueError(
                "Axiom 2 failed: hour_start_s must be strictly increasing."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_3(self) -> "GwStopgapPriceForecast":
        """
        Axiom 3: ForecastCreatedBeforeFirstHour
        ForecastCreatedS SHALL be less than the first element of HourStartS.
        """
        if self.hour_start_s and self.forecast_created_s >= self.hour_start_s[0]:
            raise ValueError(
                "Axiom 3 failed: forecast_created_s must be less than the first element of hour_start_s."
            )
        return self
