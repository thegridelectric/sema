"""gw.weather.forecast.bundle.gt axioms, proved by mutation of the word's example.

Mutations that rename a channel keep the embedded channels valid against their
own axioms, so only the bundle axiom under test fires.
"""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.forecast.bundle.gt", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.forecast.bundle.gt", "000") == {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
    }


def test_axiom_1_refuses_mismatched_slice_grids() -> None:
    def mutate(p: dict) -> None:
        wind = p["WindSpeedForecastChannel"]
        wind["TotalSlices"] = 24
        wind["SliceDurationSList"] = [7200] * 24

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_offset_not_below_period() -> None:
    def mutate(p: dict) -> None:
        p["EmitOffsetS"] = 3600

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_identical_forecast_channel_names() -> None:
    def mutate(p: dict) -> None:
        wind_obs = p["WindSpeedObservationChannel"]
        wind_obs["Name"] = "us.me.millinocket.temperature"
        wind_obs["DisplayName"] = "Millinocket temperature"
        wind_obs["Quantity"] = "Temperature"
        wind_obs["Unit"] = "FahrenheitX100"
        wind = p["WindSpeedForecastChannel"]
        wind["Name"] = "us.me.millinocket.temperature.forecast.nws.hourly"
        wind["TargetChannelName"] = "us.me.millinocket.temperature"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_refuses_unbound_target() -> None:
    def mutate(p: dict) -> None:
        p["TempObservationChannel"]["Name"] = "us.me.millinocket.temperature.tmy"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)


def test_axiom_5_refuses_wrong_quantity_target() -> None:
    def mutate(p: dict) -> None:
        temp_obs = p["TempObservationChannel"]
        temp_obs["Name"] = "us.me.millinocket.windspeed.alt"
        temp_obs["Quantity"] = "WindSpeed"
        temp_obs["Unit"] = "MilesPerHourX1000"
        temp = p["TempForecastChannel"]
        temp["Name"] = "us.me.millinocket.windspeed.alt.forecast.nws.hourly"
        temp["TargetChannelName"] = "us.me.millinocket.windspeed.alt"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 5)


def test_axiom_6_refuses_target_outside_location() -> None:
    def mutate(p: dict) -> None:
        temp_obs = p["TempObservationChannel"]
        temp_obs["LocationAlias"] = "us.vt.burlington"
        temp_obs["Name"] = "us.vt.burlington.temperature"
        temp = p["TempForecastChannel"]
        temp["Name"] = "us.vt.burlington.temperature.forecast.nws.hourly"
        temp["TargetChannelName"] = "us.vt.burlington.temperature"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 6)


def test_axiom_7_refuses_name_not_extending_location() -> None:
    def mutate(p: dict) -> None:
        p["Name"] = "us.me.millinocket.nws.hourly"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 7)
