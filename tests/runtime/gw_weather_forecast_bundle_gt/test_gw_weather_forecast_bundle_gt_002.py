"""gw.weather.forecast.bundle.gt 002 axioms, proved by mutation of the word's
example.

Mutations keep each embedded binding and channel valid against its own
axioms, so only the bundle axiom under test fires.
"""

import copy

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.forecast.bundle.gt", "002")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.forecast.bundle.gt", "002") == {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }


def test_axiom_1_refuses_empty_binding_list() -> None:
    def mutate(p: dict) -> None:
        p["BindingList"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_mismatched_slice_grids() -> None:
    def mutate(p: dict) -> None:
        wind = p["BindingList"][1]["ForecastChannel"]
        wind["TotalSlices"] = 24
        wind["SliceDurationSList"] = [7200] * 24

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_offset_not_below_period() -> None:
    def mutate(p: dict) -> None:
        p["EmitOffsetS"] = 3600

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_refuses_identical_forecast_channel_names() -> None:
    def mutate(p: dict) -> None:
        # A second copy of the temperature binding: the only axiom it breaks
        # first is the distinct forecast-channel names.
        p["BindingList"][1] = copy.deepcopy(p["BindingList"][0])

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)


def test_axiom_5_refuses_repeated_quantity() -> None:
    def mutate(p: dict) -> None:
        wind = p["BindingList"][1]
        obs = wind["ObservationChannel"]
        obs["Name"] = "kmlt.temperature.alt"
        obs["Quantity"] = "Temperature"
        obs["Unit"] = "FahrenheitX10"
        wind["ForecastChannel"]["Name"] = (
            "kmlt.temperature.alt.forecast.nws.hourly"
        )
        wind["ForecastChannel"]["TargetChannelName"] = obs["Name"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 5)


def test_axiom_6_refuses_name_with_two_further_segments() -> None:
    def mutate(p: dict) -> None:
        p["Name"] = "us.me.millinocket.forecast.raccoon"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 6)
