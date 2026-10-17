"""gw.weather.forecast.series axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.forecast.series", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.forecast.series", "000") == {1: [], 2: []}


def test_axiom_1_refuses_empty_values() -> None:
    def mutate(p: dict) -> None:
        p["Values"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_channel_without_forecast_segment() -> None:
    def mutate(p: dict) -> None:
        p["ChannelName"] = "us.me.millinocket.temperature"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)
