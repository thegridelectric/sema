"""gw.weather.archive.cmd axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.archive.cmd", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.archive.cmd", "000") == {1: [], 2: [], 3: []}


def test_axiom_1_refuses_end_not_after_start() -> None:
    def mutate(p: dict) -> None:
        p["End"] = p["Start"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_channel_off_station() -> None:
    def mutate(p: dict) -> None:
        p["ChannelNameList"][0] = "elsewhere.temperature"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_repeated_channel() -> None:
    def mutate(p: dict) -> None:
        p["ChannelNameList"].append(p["ChannelNameList"][0])

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)
