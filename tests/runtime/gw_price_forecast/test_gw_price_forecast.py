"""gw.price.forecast 000: a MarketMaker's price forecast, one price per
slot, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.gw_price_forecast import GwPriceForecast
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.price.forecast", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.price.forecast", "000") == {1: ["a", "b", "c"], 2: []}


def test_example_round_trips() -> None:
    forecast = GwPriceForecast.model_validate(EXAMPLE)
    assert forecast.price_x1000_list == [628052, 99876, 98806]
    assert (
        GwPriceForecast.model_validate(forecast.model_dump(by_alias=True)) == forecast
    )


def test_axiom_1a_refuses_no_slots() -> None:
    def mutate(p: dict) -> None:
        p["SlotStartS"] = []
        p["PriceX1000List"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, "a")


def test_axiom_1b_refuses_a_repeated_slot_start() -> None:
    def mutate(p: dict) -> None:
        p["SlotStartS"][2] = p["SlotStartS"][1]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, "b")


def test_axiom_1c_refuses_a_slot_start_off_the_five_minute_grid() -> None:
    def mutate(p: dict) -> None:
        p["SlotStartS"][2] += 60

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, "c")


def test_axiom_2_refuses_a_price_list_one_value_short() -> None:
    def mutate(p: dict) -> None:
        p["PriceX1000List"] = p["PriceX1000List"][:2]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)
