from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import GwZoneEmitterType
from sema.runtime.enums import ZoneSetpointSource
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.gw1_zone_thermostat import Gw1ZoneThermostat


class Gw1ZoneCallCircuit(SemaType):
    """Sema: https://schemas.electricity.works/types/gw1.zone.call.circuit/000"""

    circuit_position: PositiveInt
    serves_zone: SpaceheatName
    emitter_type: GwZoneEmitterType
    can_cool: bool
    setpoint_source: ZoneSetpointSource
    thermostat: Gw1ZoneThermostat
    whitewire_channel_name: SpaceheatName
    floor_temp_channel_name: SpaceheatName | None = None
    failsafe_relay_node: SpaceheatName
    ops_relay_node: SpaceheatName
    type_name: Literal["gw1.zone.call.circuit"] = "gw1.zone.call.circuit"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "Gw1ZoneCallCircuit":
        """
        Axiom 1: OnlyFanCoilsCool If EmitterType is not FanCoil, CanCool SHALL be false.
        """
        # String comparison: the enum class name differs under a snapshot's
        # local names.
        if str(self.emitter_type) != "FanCoil" and self.can_cool:
            raise ValueError(
                f"Axiom 1 (OnlyFanCoilsCool) failed: EmitterType is "
                f"{self.emitter_type}, so CanCool SHALL be false."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "Gw1ZoneCallCircuit":
        """
        Axiom 2: ReadSetpointNeedsCommsStat If SetpointSource is FromThermostat,
        Thermostat.Kind SHALL NOT be MechanicalDial.
        """
        # String comparison, not an enum import: ThermostatKind is not a field
        # enum of this type, and an absolute sema.runtime import would break
        # inside a restricted snapshot package.
        if (
            self.setpoint_source == ZoneSetpointSource.FromThermostat
            and self.thermostat.kind == "MechanicalDial"
        ):
            raise ValueError(
                "Axiom 2 (ReadSetpointNeedsCommsStat) failed: SetpointSource is "
                "FromThermostat, so Thermostat.Kind SHALL NOT be MechanicalDial."
            )
        return self
