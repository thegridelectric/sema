"""gw.weather.forecast 001 axioms, proved by mutation of the word's example.

Mutations keep each embedded series valid against its own axioms, so only the
forecast axiom under test fires.
"""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.forecast", "001")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.forecast", "001") == {
        1: [],
        2: [],
        3: [],
        4: [],
    }


def test_axiom_1_refuses_empty_series_list() -> None:
    def mutate(p: dict) -> None:
        p["SeriesList"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_unequal_value_lengths() -> None:
    def mutate(p: dict) -> None:
        p["SeriesList"][1]["Values"] = p["SeriesList"][1]["Values"][:1]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_identical_channel_names() -> None:
    def mutate(p: dict) -> None:
        p["SeriesList"][1]["ChannelName"] = p["SeriesList"][0]["ChannelName"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_refuses_repeated_quantity() -> None:
    def mutate(p: dict) -> None:
        p["SeriesList"][1]["Quantity"] = p["SeriesList"][0]["Quantity"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)
