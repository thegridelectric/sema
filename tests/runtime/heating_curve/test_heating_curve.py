"""heating.curve 000: the example validates and the two anchor axioms refuse.

The word's own example is the vanilla curve. Each rejecting test mutates a
copy so that exactly one rule fires.
"""

import json
from pathlib import Path
from typing import Any, Callable

import pytest
import yaml
from pydantic import ValidationError

from sema.runtime.types.heating_curve import HeatingCurve

SCHEMA = (
    Path(__file__).resolve().parents[3]
    / "definitions"
    / "types"
    / "heating.curve"
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


def test_vanilla_is_a_heating_curve(vanilla: dict[str, Any]) -> None:
    c = HeatingCurve.model_validate(vanilla)
    assert c.dd_rswt_f >= c.intermediate_rswt_f
    assert c.dd_power_kw >= c.intermediate_power_kw
    assert c.rho_times100 > 0


def test_equal_anchors_pass(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DdRswtF"] = d["IntermediateRswtF"]
        d["DdPowerKw"] = d["IntermediatePowerKw"]

    HeatingCurve.model_validate(mutated(vanilla, mutate))


def test_axiom_1_design_day_rswt_below_intermediate(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DdRswtF"] = d["IntermediateRswtF"] - 1

    with pytest.raises(ValidationError, match="Axiom 1"):
        HeatingCurve.model_validate(mutated(vanilla, mutate))


def test_axiom_2_design_day_power_below_intermediate(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DdPowerKw"] = d["IntermediatePowerKw"] / 2

    with pytest.raises(ValidationError, match="Axiom 2"):
        HeatingCurve.model_validate(mutated(vanilla, mutate))


def test_rho_must_be_positive(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["RhoTimes100"] = 0

    with pytest.raises(ValidationError):
        HeatingCurve.model_validate(mutated(vanilla, mutate))
