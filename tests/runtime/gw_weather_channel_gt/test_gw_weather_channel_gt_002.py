"""gw.weather.channel.gt 002 axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.channel.gt", "002")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.channel.gt", "002") == {1: [], 2: []}


def test_axiom_1_refuses_name_not_derived_from_station_and_quantity() -> None:
    def mutate(p: dict) -> None:
        p["Name"] = "kmemilli18.temperature"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_offset_not_below_period() -> None:
    def mutate(p: dict) -> None:
        p["EmitOffsetS"] = 3600

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)
