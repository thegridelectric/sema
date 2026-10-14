"""gw.weather.forecast.channel.gt axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.forecast.channel.gt", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.forecast.channel.gt", "000") == {
        1: [],
        2: [],
        3: [],
        4: [],
    }


def test_axiom_1_refuses_slice_count_mismatch() -> None:
    def mutate(p: dict) -> None:
        p["TotalSlices"] = 3

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_duration_inconsistency() -> None:
    def mutate(p: dict) -> None:
        p["ForecastDurationMinutes"] = 121

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_slice_not_multiple_of_quantum() -> None:
    def mutate(p: dict) -> None:
        p["SliceDurationSList"] = [3500, 3700]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_refuses_name_without_forecast_infix() -> None:
    def mutate(p: dict) -> None:
        p["Name"] = "us.me.millinocket.temperature.nws"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)
