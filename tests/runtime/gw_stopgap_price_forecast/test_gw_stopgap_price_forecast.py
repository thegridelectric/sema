"""gw.stopgap.price.forecast axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.stopgap.price.forecast", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.stopgap.price.forecast", "000") == {
        1: [],
        2: [],
        3: [],
    }


def test_axiom_1_refuses_unequal_list_lengths() -> None:
    def mutate(p: dict) -> None:
        p["DistList"] = p["DistList"][:1]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_non_increasing_hours() -> None:
    def mutate(p: dict) -> None:
        p["HourStartS"] = list(reversed(p["HourStartS"]))

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_forecast_created_after_first_hour() -> None:
    def mutate(p: dict) -> None:
        p["ForecastCreatedS"] = p["HourStartS"][0]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)
