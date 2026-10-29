"""gw.circulator 000: the example validates and the input axiom refuses.

The vanilla circulator is the word's own example. Each rejecting test mutates
a copy so that exactly one rule fires.
"""

import json
from pathlib import Path
from typing import Any, Callable

import pytest
import yaml
from pydantic import ValidationError

from sema.runtime.types.gw_circulator import GwCirculator

SCHEMA = (
    Path(__file__).resolve().parents[3]
    / "definitions"
    / "types"
    / "gw.circulator"
    / "000.yaml"
)


@pytest.fixture(scope="module")
def vanilla() -> dict[str, Any]:
    return json.loads(yaml.safe_load(SCHEMA.read_text())["examples"][0])


def mutated(
    vanilla: dict[str, Any], mutate: Callable[[dict[str, Any]], None]
) -> dict[str, Any]:
    d = json.loads(json.dumps(vanilla))
    mutate(d)
    return d


def test_vanilla_is_a_circulator(vanilla: dict[str, Any]) -> None:
    c = GwCirculator.model_validate(vanilla)
    assert c.pump_node_name == "dist-pump"
    assert c.role == "Dist"
    assert c.running_channel_name == "dist-pump-running"


def test_ct_only_input_validates(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        del d["PowerChannelName"]
        d["CtChannelName"] = "dist-pump-ct"

    c = GwCirculator.model_validate(mutated(vanilla, mutate))
    assert c.power_channel_name is None
    assert c.ct_channel_name == "dist-pump-ct"


def test_optional_sensing_may_be_absent(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        del d["FlowChannelName"]
        del d["ZeroTenNodeName"]

    c = GwCirculator.model_validate(mutated(vanilla, mutate))
    assert c.flow_channel_name is None
    assert c.zero_ten_node_name is None


def test_axiom_1_no_input_declared(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        del d["PowerChannelName"]

    with pytest.raises(ValidationError, match="Axiom 1"):
        GwCirculator.model_validate(mutated(vanilla, mutate))


def test_unknown_role_decodes_to_default(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["Role"] = "Buffer"

    assert GwCirculator.model_validate(mutated(vanilla, mutate)).role == "Unknown"
