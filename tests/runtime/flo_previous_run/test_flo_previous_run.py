"""flo.previous.run 000: the cleared pair and the path it led to, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.flo_previous_run import FloPreviousRun
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("flo.previous.run", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.previous.run", "000") == {1: []}


def test_example_round_trips() -> None:
    r = FloPreviousRun.model_validate(EXAMPLE)
    assert r.cleared_pair.quantity_x1000 == 4200
    assert FloPreviousRun.model_validate(r.model_dump(by_alias=True)) == r


def test_axiom_1_refuses_a_path_whose_first_step_is_not_the_bid() -> None:
    def mutate(p: dict) -> None:
        p["Path"]["HpAvgWList"][0] = 4199

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_1_scales_avg_mw_to_watts() -> None:
    def mutate(p: dict) -> None:
        p["QuantityUnit"] = "AvgMW"
        p["ClearedPair"]["QuantityX1000"] = 4
        p["Path"]["HpAvgWList"][0] = 4000

    FloPreviousRun.model_validate(mutated(EXAMPLE, mutate))
