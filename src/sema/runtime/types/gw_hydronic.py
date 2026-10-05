from typing import Literal, Self
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import GwPrimaryFlowSource
from sema.runtime.enums import GwPrimaryPumpOwner
from sema.runtime.enums import GwRefrigerantCycle
from sema.runtime.property_format import NonNegativeInt
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.gw1_hvac_zone import Gw1HvacZone
from sema.runtime.types.gw1_zone_call_circuit import Gw1ZoneCallCircuit


class GwHydronic(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.hydronic/000"""

    zones: list[Gw1HvacZone]
    zone_call_circuits: list[Gw1ZoneCallCircuit]
    total_store_tanks: NonNegativeInt
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
        a. TotalStoreTanks SHALL be at most 6.
        b. The number of Zones SHALL be between 1 and 6 inclusive.
        """
        if self.total_store_tanks > 6:
            raise ValueError(
                "Axiom 1 (Cardinality) failed: TotalStoreTanks "
                f"({self.total_store_tanks}) must be at most 6."
            )
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
        Zones. b. No two circuits SHALL share a CircuitPosition.
        c. No two zones SHALL share a Name. d. Every zone in Zones SHALL be
        the ServesZone of at least one circuit.
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
        if len(positions) != len(set(positions)):
            raise ValueError(
                "Axiom 2 (CircuitResolution) failed: CircuitPosition values "
                f"{positions} are not distinct."
            )
        names = [z.name for z in self.zones]
        if len(names) != len(set(names)):
            raise ValueError(
                f"Axiom 2 (CircuitResolution) failed: zone Names {names} are not distinct."
            )
        served = {c.serves_zone for c in circuits}
        unserved = [name for name in names if name not in served]
        if unserved:
            raise ValueError(
                f"Axiom 2 (CircuitResolution) failed: zones {unserved} are served by no circuit."
            )
        return self
