"""market.terms 000: a MarketMaker's statement of the dispatch terms its
market runs under from a slot boundary, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.market_terms import MarketTerms
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("market.terms", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("market.terms", "000") == {1: []}


def test_example_round_trips() -> None:
    terms = MarketTerms.model_validate(EXAMPLE)
    assert terms.effective_s % 3600 == 0
    assert MarketTerms.model_validate(terms.model_dump(by_alias=True)) == terms


def test_axiom_1_refuses_an_effective_time_inside_a_slot() -> None:
    def mutate(p: dict) -> None:
        p["EffectiveS"] += 300

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_1_refuses_a_product_with_no_slot_length() -> None:
    def mutate(p: dict) -> None:
        p["MarketProductName"] = "unknown"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_a_five_minute_product_takes_a_five_minute_boundary() -> None:
    def mutate(p: dict) -> None:
        p["MarketProductName"] = "rt5gate5"
        p["EffectiveS"] += 300

    MarketTerms.model_validate(mutated(EXAMPLE, mutate))
