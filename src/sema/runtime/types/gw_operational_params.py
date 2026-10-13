from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1ServiceMode
from sema.runtime.enums import GwStandbyPosture
from sema.runtime.enums import SiegLoopStrategy
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import NonNegativeInt
from sema.runtime.property_format import PositiveFloat
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.capture_tuning import CaptureTuning
from sema.runtime.types.cop_curve import CopCurve
from sema.runtime.types.gw_dispatch_hold import GwDispatchHold
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
    standby: bool
    standby_posture: GwStandbyPosture
    energized_standby_relays: list[SpaceheatName]
    service_mode: Gw1ServiceMode
    dispatch_hold: GwDispatchHold
    cop_curve: CopCurve
    heating_curve: HeatingCurve
    hp_turn_on_minutes: PositiveInt
    hp_max_kw_el: PositiveFloat
    load_overestimation_percent: NonNegativeInt
    uses_backup_when_cold: bool
    horizon_hours: PositiveInt
    weather_bundle_name: LeftRightDot
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

    @model_validator(mode="after")
    def check_axiom_3(self) -> "GwOperationalParams":
        """
        Axiom 3: StandbyImpliesOperatorHold
        If Standby is true, DispatchHold.OperatorHold SHALL be true.
        """
        if self.standby and not self.dispatch_hold.operator_hold:
            raise ValueError(
                "Axiom 3 (StandbyImpliesOperatorHold) failed: Standby requires "
                "DispatchHold.OperatorHold."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_4(self) -> "GwOperationalParams":
        """
        Axiom 4: PostureRelaysPerFamily
        StandbyPosture fixes EnergizedStandbyRelays for the family named by
        FamilyParams.TypeName: a. If StandbyPosture is MonitorOnly,
        EnergizedStandbyRelays SHALL be empty. b. If FamilyParams.TypeName is
        gw.house0.family.params and StandbyPosture is NoHeatingOrCooling,
        EnergizedStandbyRelays SHALL be exactly hp-failsafe-relay and
        aquastat-ctrl-relay. c. If FamilyParams.TypeName is gw.nolan.family.params
        and StandbyPosture is NoHeatingOrCooling, EnergizedStandbyRelays SHALL be
        empty.
        """
        posture = self.standby_posture
        relays = set(self.energized_standby_relays)
        family = self.family_params.type_name
        if posture is GwStandbyPosture.MonitorOnly and relays:
            raise ValueError(
                "Axiom 4 (PostureRelaysPerFamily) failed: MonitorOnly requires "
                "an empty EnergizedStandbyRelays."
            )
        if posture is GwStandbyPosture.NoHeatingOrCooling:
            expected = {
                "gw.house0.family.params": {"hp-failsafe-relay", "aquastat-ctrl-relay"},
                "gw.nolan.family.params": set(),
            }[family]
            if relays != expected:
                raise ValueError(
                    "Axiom 4 (PostureRelaysPerFamily) failed: NoHeatingOrCooling "
                    f"for {family} requires EnergizedStandbyRelays {sorted(expected)}, "
                    f"got {sorted(relays)}."
                )
        return self

    @model_validator(mode="after")
    def check_axiom_5(self) -> "GwOperationalParams":
        """
        Axiom 5: StandbyHoldsFullSend
        If Standby is true and FamilyParams.TypeName is gw.house0.family.params,
        FamilyParams.SiegLoopStrategy SHALL be HoldFullSend.
        """
        family = self.family_params
        if (
            self.standby
            and isinstance(family, GwHouse0FamilyParams)
            and family.sieg_loop_strategy is not SiegLoopStrategy.HoldFullSend
        ):
            raise ValueError(
                "Axiom 5 (StandbyHoldsFullSend) failed: Standby requires "
                f"SiegLoopStrategy HoldFullSend, got {family.sieg_loop_strategy}."
            )
        return self
