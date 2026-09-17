from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1ActuationAuthority
from sema.runtime.enums import Gw1ServiceMode
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import NonNegativeInt
from sema.runtime.property_format import PositiveFloat
from sema.runtime.property_format import PositiveInt
from sema.runtime.types.capture_tuning import CaptureTuning
from sema.runtime.types.cop_curve import CopCurve
from sema.runtime.types.gw_house0_family_params import GwHouse0FamilyParams
from sema.runtime.types.gw_nolan_family_params import GwNolanFamilyParams
from sema.runtime.types.gw_tou_tariff import GwTouTariff
from sema.runtime.types.heating_curve import HeatingCurve
from sema.runtime.types.zero_ten_power_on import ZeroTenPowerOn


class GwOperationalParams(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.operational.params/000"""

    scada_alias: LeftRightDot
    family_params: GwHouse0FamilyParams | GwNolanFamilyParams
    capture_tuning_list: list[CaptureTuning]
    zero_ten_power_on_list: list[ZeroTenPowerOn]
    actuation_authority: Gw1ActuationAuthority
    service_mode: Gw1ServiceMode
    cop_curve: CopCurve
    heating_curve: HeatingCurve
    hp_turn_on_minutes: PositiveInt
    hp_max_kw_el: PositiveFloat
    load_overestimation_percent: NonNegativeInt
    oil_boiler_backup: bool
    horizon_hours: PositiveInt
    tariff: GwTouTariff
    type_name: Literal["gw.operational.params"] = "gw.operational.params"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwOperationalParams":
        """
        Axiom 1: CaptureTuningChannelUniqueness
        ChannelName SHALL be unique across CaptureTuningList.
        """
        names = [ct.channel_name for ct in self.capture_tuning_list]
        if len(names) != len(set(names)):
            raise ValueError(
                "Axiom 1 (CaptureTuningChannelUniqueness) failed: ChannelName "
                "must be unique across CaptureTuningList."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwOperationalParams":
        """
        Axiom 2: ZeroTenPowerOnNodeUniqueness
        NodeName SHALL be unique across ZeroTenPowerOnList.
        """
        names = [z.node_name for z in self.zero_ten_power_on_list]
        if len(names) != len(set(names)):
            raise ValueError(
                "Axiom 2 (ZeroTenPowerOnNodeUniqueness) failed: NodeName "
                "must be unique across ZeroTenPowerOnList."
            )
        return self
