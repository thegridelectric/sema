"""gw.weather.forecast 002: ForecastUid, and the 001 axioms proved again by mutation."""

import pytest
from pydantic import ValidationError

from sema.runtime.codec import default_codec
from sema.runtime.types.gw_weather_forecast import GwWeatherForecast
from sema.runtime.types.old_versions.gw_weather_forecast_001 import GwWeatherForecast001
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.forecast", "002")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.forecast", "002") == {1: [], 2: [], 3: [], 4: []}


def test_example_round_trips_with_its_uid() -> None:
    f = GwWeatherForecast.model_validate(EXAMPLE)
    assert str(f.forecast_uid) == "5f1c2b3a-8d4e-4f60-9a7b-1c2d3e4f5a6b"
    assert GwWeatherForecast.model_validate(f.model_dump(by_alias=True)) == f


def test_forecast_uid_is_required() -> None:
    def mutate(p: dict) -> None:
        del p["ForecastUid"]

    with pytest.raises(ValidationError):
        GwWeatherForecast.model_validate(mutated(EXAMPLE, mutate))


def test_001_does_not_upgrade_without_the_service() -> None:
    old = example("gw.weather.forecast", "001")
    with pytest.raises(ValueError, match="(?i)context"):
        GwWeatherForecast001.model_validate(old).upgrade()


def test_axiom_1_refuses_empty_series_list() -> None:
    def mutate(p: dict) -> None:
        p["SeriesList"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_unequal_value_lengths() -> None:
    def mutate(p: dict) -> None:
        p["SeriesList"][1]["Values"] = p["SeriesList"][1]["Values"][:1]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_identical_channel_names() -> None:
    def mutate(p: dict) -> None:
        p["SeriesList"][1]["ChannelName"] = p["SeriesList"][0]["ChannelName"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_refuses_repeated_quantity() -> None:
    def mutate(p: dict) -> None:
        p["SeriesList"][1]["Quantity"] = p["SeriesList"][0]["Quantity"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)
