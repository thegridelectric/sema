"""Rejecting tests for gw1.zone.call.circuit/000's axioms.

The vanilla circuit is the one the gw.hydronic example carries. Each test
mutates a copy of it so that exactly one axiom fires.
"""

import json
from pathlib import Path
from typing import Any, Callable

import pytest
import yaml

from sema.runtime.types.gw1_zone_call_circuit import Gw1ZoneCallCircuit

HYDRONIC = (
    Path(__file__).resolve().parents[3]
    / "definitions"
    / "types"
    / "gw.hydronic"
    / "000.yaml"
)


@pytest.fixture(scope="module")
def vanilla() -> dict[str, Any]:
    schema = yaml.safe_load(HYDRONIC.read_text())
    hydronic = json.loads(schema["examples"][0])
    return hydronic["ZoneCallCircuits"][0]


def mutated(
    vanilla: dict[str, Any], mutate: Callable[[dict[str, Any]], None]
) -> dict[str, Any]:
    d = json.loads(json.dumps(vanilla))
    mutate(d)
    return d


def reject(
    vanilla: dict[str, Any], mutate: Callable[[dict[str, Any]], None], axiom: str
) -> None:
    with pytest.raises(ValueError, match=axiom):
        Gw1ZoneCallCircuit.model_validate(mutated(vanilla, mutate))


def test_vanilla_circuit_is_a_gw1_zone_call_circuit(vanilla: dict[str, Any]) -> None:
    circuit = Gw1ZoneCallCircuit.model_validate(vanilla)
    assert circuit.type_name == "gw1.zone.call.circuit"
    assert circuit.emitter_type == "RadiantSlab"


@pytest.mark.parametrize(
    "emitter_type",
    ["Other", "RadiantSlab"],
)
def test_axiom_1_only_fan_coils_cool(
    vanilla: dict[str, Any], emitter_type: str
) -> None:
    """Every emitter but a fan coil moves heat one way, so CanCool SHALL be false."""

    def mutate(d: dict[str, Any]) -> None:
        d["EmitterType"] = emitter_type
        d["CanCool"] = True

    reject(vanilla, mutate, "Axiom 1")


def test_axiom_1_a_fan_coil_may_cool(vanilla: dict[str, Any]) -> None:
    """A fan coil is the one emitter a circuit may cool through."""

    def mutate(d: dict[str, Any]) -> None:
        d["EmitterType"] = "FanCoil"
        d["CanCool"] = True
        d.pop("FloorTempChannelName", None)

    Gw1ZoneCallCircuit.model_validate(mutated(vanilla, mutate))


def test_axiom_2_read_setpoint_needs_comms_stat(vanilla: dict[str, Any]) -> None:
    """Reading a setpoint off a mechanical dial is not possible."""

    def mutate(d: dict[str, Any]) -> None:
        d["SetpointSource"] = "FromThermostat"
        d["Thermostat"]["Kind"] = "MechanicalDial"

    reject(vanilla, mutate, "Axiom 2")


def test_floor_temp_channel_name_is_optional(vanilla: dict[str, Any]) -> None:
    """The circuit word itself does not require a floor channel; the layout words
    do, for the emitters that sit in a floor."""

    def mutate(d: dict[str, Any]) -> None:
        d.pop("FloorTempChannelName", None)

    Gw1ZoneCallCircuit.model_validate(mutated(vanilla, mutate))
