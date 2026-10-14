"""gw.weather.observation axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.observation", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.observation", "000") == {1: [], 2: ["a", "b"]}


def test_axiom_1_refuses_identical_channel_names() -> None:
    def mutate(p: dict) -> None:
        p["WindSpeedChannelName"] = p["TempChannelName"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_a_refuses_temp_channel_outside_location() -> None:
    def mutate(p: dict) -> None:
        p["TempChannelName"] = "us.vt.burlington.temperature"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2, clause="a")


def test_axiom_2_b_refuses_windspeed_channel_outside_location() -> None:
    def mutate(p: dict) -> None:
        p["WindSpeedChannelName"] = "us.vt.burlington.windspeed"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2, clause="b")
