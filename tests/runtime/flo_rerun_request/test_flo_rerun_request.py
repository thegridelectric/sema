"""flo.rerun.request 000: laptop re-solve body wrapping flo.params."""

import pytest
from pydantic import ValidationError

from sema.runtime.types.flo_rerun_request import FloRerunRequest
from tests.runtime.refusal import axioms, example, mutated

EXAMPLE = example("flo.rerun.request", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.rerun.request", "000") == {1: [], 2: []}


def test_example_round_trips() -> None:
    r = FloRerunRequest.model_validate(EXAMPLE)
    assert r.hp_forced_off_steps == [1]
    assert FloRerunRequest.model_validate(r.model_dump(by_alias=True)) == r


def test_axiom_1_step_out_of_range() -> None:
    def mutate(p: dict) -> None:
        p["HpForcedOnSteps"] = [99]

    with pytest.raises(ValidationError, match="(?i)axiom 1"):
        FloRerunRequest.model_validate(mutated(EXAMPLE, mutate))


def test_axiom_2_step_in_both_lists() -> None:
    def mutate(p: dict) -> None:
        p["HpForcedOnSteps"] = [1]

    with pytest.raises(ValidationError, match="(?i)axiom 2"):
        FloRerunRequest.model_validate(mutated(EXAMPLE, mutate))
