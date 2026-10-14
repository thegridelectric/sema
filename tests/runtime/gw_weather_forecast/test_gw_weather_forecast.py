"""gw.weather.forecast axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.forecast", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.forecast", "000") == {
        1: [],
        2: [],
        3: [],
        4: ["a", "b", "c"],
    }


def test_axiom_1_refuses_empty_value_lists() -> None:
    def mutate(p: dict) -> None:
        p["TempValues"] = []
        p["WindSpeedValues"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_unequal_value_lengths() -> None:
    def mutate(p: dict) -> None:
        p["WindSpeedValues"] = p["WindSpeedValues"][:1]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_identical_channel_names() -> None:
    def mutate(p: dict) -> None:
        p["WindSpeedChannelName"] = p["TempChannelName"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_a_refuses_bundle_name_without_forecast_segment() -> None:
    def mutate(p: dict) -> None:
        p["BundleName"] = "us.me.millinocket.nws.hourly"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, clause="a")


def test_axiom_4_b_refuses_temp_channel_without_forecast_segment() -> None:
    def mutate(p: dict) -> None:
        p["TempChannelName"] = "us.me.millinocket.temperature"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, clause="b")


def test_axiom_4_c_refuses_windspeed_channel_without_forecast_segment() -> None:
    def mutate(p: dict) -> None:
        p["WindSpeedChannelName"] = "us.me.millinocket.windspeed"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, clause="c")
