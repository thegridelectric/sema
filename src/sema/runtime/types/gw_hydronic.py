from typing import Literal, Self
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import GwPrimaryFlowSource
from sema.runtime.enums import GwPrimaryPumpOwner
from sema.runtime.enums import GwRefrigerantCycle
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.gw1_hvac_zone import Gw1HvacZone
from sema.runtime.types.gw1_zone_call_circuit import Gw1ZoneCallCircuit
from sema.runtime.types.gw_water_store import GwWaterStore


class GwHydronic(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.hydronic/000"""

    zones: list[Gw1HvacZone]
    zone_call_circuits: list[Gw1ZoneCallCircuit]
    water_store: GwWaterStore | None = None
    primary_flow_source: GwPrimaryFlowSource
    primary_pump_owner: GwPrimaryPumpOwner
    refrigerant_cycle: GwRefrigerantCycle
    hp_command_node_name: SpaceheatName | None = None
    type_name: Literal["gw.hydronic"] = "gw.hydronic"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom 1: Cardinality
        The number of Zones SHALL be between 1 and 6 inclusive.
        """
        if not 1 <= len(self.zones) <= 6:
            raise ValueError(
                "Axiom 1 (Cardinality) failed: number of Zones "
                f"({len(self.zones)}) must be between 1 and 6 inclusive."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> Self:
        """
        Axiom 2: CircuitResolution
        a. Every circuit's ServesZone SHALL equal the Name of a zone in
        Zones. b. The circuit at 1-based place i in ZoneCallCircuits SHALL
        have CircuitPosition i.
        c. No two zones SHALL share a Name.
        """
        circuits = self.zone_call_circuits or []
        zone_names = {z.name for z in self.zones}
        for c in circuits:
            if c.serves_zone not in zone_names:
                raise ValueError(
                    "Axiom 2 (CircuitResolution) failed: ServesZone "
                    f"{c.serves_zone!r} does not name a zone in Zones."
                )
        positions = [c.circuit_position for c in circuits]
        if positions != list(range(1, len(circuits) + 1)):
            raise ValueError(
                "Axiom 2 (CircuitResolution) failed: CircuitPosition values "
                f"{positions} are not each circuit's 1-based place in ZoneCallCircuits."
            )
        names = [z.name for z in self.zones]
        if len(names) != len(set(names)):
            raise ValueError(
                f"Axiom 2 (CircuitResolution) failed: zone Names {names} are not distinct."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_3(self) -> Self:
        """
        Axiom 3: PrimaryCircuit
        a. Every zone's PrimaryCircuitPosition SHALL equal the
        CircuitPosition of a circuit whose ServesZone equals the zone's
        Name. b. That circuit SHALL carry SetpointChannelName.
        """
        circuits = {c.circuit_position: c for c in (self.zone_call_circuits or [])}
        for zone in self.zones:
            primary = circuits.get(zone.primary_circuit_position)
            if primary is None or primary.serves_zone != zone.name:
                raise ValueError(
                    f"Axiom 3 (PrimaryCircuit) failed: zone {zone.name!r} names "
                    f"PrimaryCircuitPosition {zone.primary_circuit_position}, which is "
                    "not the position of a circuit serving it."
                )
            if not primary.setpoint_channel_name:
                raise ValueError(
                    f"Axiom 3 (PrimaryCircuit) failed: zone {zone.name!r}'s primary "
                    f"circuit {primary.name!r} carries no SetpointChannelName."
                )
        return self

    @model_validator(mode="after")
    def check_axiom_4(self) -> Self:
        """
        Axiom 4: CircuitDistinctness
        a. No two circuits SHALL share a Name. b. No two circuits SHALL
        share a WhitewireChannelName. c. No two circuits SHALL share a
        SetpointChannelName. d. No two circuits SHALL share a
        TempChannelName. e. No two circuits SHALL share a FailsafeRelayNode.
        f. No two circuits SHALL share an OpsRelayNode.
        """
        circuits = self.zone_call_circuits or []
        for field, values in (
            ("Name", [c.name for c in circuits]),
            ("WhitewireChannelName", [c.whitewire_channel_name for c in circuits]),
            (
                "SetpointChannelName",
                [c.setpoint_channel_name for c in circuits if c.setpoint_channel_name],
            ),
            (
                "TempChannelName",
                [c.temp_channel_name for c in circuits if c.temp_channel_name],
            ),
            ("FailsafeRelayNode", [c.failsafe_relay_node for c in circuits]),
            ("OpsRelayNode", [c.ops_relay_node for c in circuits]),
        ):
            if len(values) != len(set(values)):
                raise ValueError(
                    f"Axiom 4 (CircuitDistinctness) failed: {field} values {values} "
                    "are not distinct."
                )
        return self
