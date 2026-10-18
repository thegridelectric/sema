"""gw.weather.station.gt axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.station.gt", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.station.gt", "000") == {1: ["a", "b"]}


def test_axiom_1_a_refuses_latitude_out_of_bounds() -> None:
    def mutate(p: dict) -> None:
        p["LatitudeMicrodegrees"] = 95_000_000

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, clause="a")


def test_axiom_1_b_refuses_longitude_out_of_bounds() -> None:
    def mutate(p: dict) -> None:
        p["LongitudeMicrodegrees"] = -190_000_000

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, clause="b")
