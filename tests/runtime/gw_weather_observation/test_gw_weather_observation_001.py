"""gw.weather.observation 001 axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.observation", "001")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.observation", "001") == {1: [], 2: [], 3: [], 4: []}


def test_axiom_1_refuses_empty_reading_list() -> None:
    def mutate(p: dict) -> None:
        p["ReadingList"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_identical_channel_names() -> None:
    def mutate(p: dict) -> None:
        p["ReadingList"][1]["ChannelName"] = p["ReadingList"][0]["ChannelName"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_repeated_quantity() -> None:
    def mutate(p: dict) -> None:
        p["ReadingList"][1]["Quantity"] = p["ReadingList"][0]["Quantity"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_refuses_channel_outside_station() -> None:
    def mutate(p: dict) -> None:
        p["ReadingList"][1]["ChannelName"] = "kmemilli18.windspeed"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)
