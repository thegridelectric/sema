"""gw.hydronic 000: the circulator list and its distinctness axiom.

The vanilla hydronic block is the word's own example. Each rejecting test
mutates a copy so that exactly one rule fires.
"""

import json
from pathlib import Path
from typing import Any, Callable

import pytest
import yaml
from pydantic import ValidationError

from sema.runtime.types.gw_hydronic import GwHydronic

SCHEMA = (
    Path(__file__).resolve().parents[3]
    / "definitions"
    / "types"
    / "gw.hydronic"
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


def test_vanilla_is_a_hydronic_block(vanilla: dict[str, Any]) -> None:
    h = GwHydronic.model_validate(vanilla)
    assert [c.pump_node_name for c in h.circulators] == [
        "dist-pump",
        "primary-pump",
        "store-pump",
    ]


def test_circulators_are_required(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        del d["Circulators"]

    with pytest.raises(ValidationError):
        GwHydronic.model_validate(mutated(vanilla, mutate))


def test_axiom_5_two_circulators_on_one_pump(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["Circulators"][1]["PumpNodeName"] = "dist-pump"

    with pytest.raises(ValidationError, match="Axiom 5"):
        GwHydronic.model_validate(mutated(vanilla, mutate))
