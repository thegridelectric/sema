"""flo.path.penalties.bruce 000: the per-step penalties, the terminal cost and the path cost, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.flo_path_penalties_bruce import FloPathPenaltiesBruce
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("flo.path.penalties.bruce", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.path.penalties.bruce", "000") == {1: [], 2: []}


def test_example_round_trips() -> None:
    r = FloPathPenaltiesBruce.model_validate(EXAMPLE)
    assert r.terminal_cost_usd == 1.87
    assert FloPathPenaltiesBruce.model_validate(r.model_dump(by_alias=True)) == r


def test_axiom_1_refuses_a_short_penalty_list() -> None:
    def mutate(p: dict) -> None:
        p["ShortCyclePenaltyUsdList"] = [0.0, 0.0]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_a_terminal_cost_at_the_bound_is_accepted() -> None:
    def mutate(p: dict) -> None:
        p["TerminalCostUsd"] = p["TerminalCostEmptyStoreUsd"]

    FloPathPenaltiesBruce.model_validate(mutated(EXAMPLE, mutate))


def test_axiom_2_refuses_a_terminal_cost_above_the_empty_store_cost() -> None:
    def mutate(p: dict) -> None:
        p["TerminalCostUsd"] = p["TerminalCostEmptyStoreUsd"] + 0.01

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)
