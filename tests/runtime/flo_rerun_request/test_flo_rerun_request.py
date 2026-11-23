"""flo.rerun.request 003: laptop re-solve body wrapping flo.params."""

import pytest
from pydantic import ValidationError

from sema.runtime.types.flo_rerun_request import FloRerunRequest
from sema.runtime.types.old_versions.flo_rerun_request_000 import FloRerunRequest000
from sema.runtime.types.old_versions.flo_rerun_request_001 import FloRerunRequest001
from sema.runtime.types.old_versions.flo_rerun_request_002 import FloRerunRequest002
from tests.runtime.refusal import axioms, example, mutated

EXAMPLE = example("flo.rerun.request", "003")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.rerun.request", "003") == {1: [], 2: []}


def test_example_round_trips() -> None:
    r = FloRerunRequest.model_validate(EXAMPLE)
    assert r.hp_forced_off_steps == [1]
    assert FloRerunRequest.model_validate(r.model_dump(by_alias=True)) == r


def test_axiom_1_step_out_of_range() -> None:
    def mutate(p: dict) -> None:
        p["HpForcedOnSteps"] = [99]

    with pytest.raises(ValidationError, match="(?i)axiom 1"):
        FloRerunRequest.model_validate(mutated(EXAMPLE, mutate))


def test_a_000_request_lifts_params_002_with_the_penalty_off() -> None:
    old = example("flo.rerun.request", "000")
    upgraded = FloRerunRequest000.model_validate(old).upgrade()
    assert upgraded.version == "001"
    assert upgraded.params.version == "003"
    assert upgraded.params.tuning.version == "002"
    assert upgraded.params.tuning.unmet_load_penalty_enabled is False
    assert upgraded.params.tuning.unmet_load_penalty_weight == 10


def test_axiom_2_step_in_both_lists() -> None:
    def mutate(p: dict) -> None:
        p["HpForcedOnSteps"] = [1]

    with pytest.raises(ValidationError, match="(?i)axiom 2"):
        FloRerunRequest.model_validate(mutated(EXAMPLE, mutate))


def test_a_001_request_lifts_params_003_to_004() -> None:
    old = example("flo.rerun.request", "001")
    upgraded = FloRerunRequest001.model_validate(old).upgrade()
    assert upgraded.version == "002"
    assert upgraded.params.version == "004"
    assert upgraded.params.tuning.version == "003"
    assert upgraded.params.tuning.experimental == {
        "UnmetLoadPenaltyEnabled": True,
        "UnmetLoadPenaltyWeight": 10.0,
    }


def test_a_002_request_lifts_params_004_to_005() -> None:
    old = example("flo.rerun.request", "002")
    upgraded = FloRerunRequest002.model_validate(old).upgrade()
    assert isinstance(upgraded, FloRerunRequest)
    assert upgraded.version == "003"
    assert upgraded.params.version == "005"
    assert upgraded.params.cop_lwt_minus_oat_coeff == old["Params"]["CopLwtCoeff"]
    assert not hasattr(upgraded.params, "cop_oat_coeff")
