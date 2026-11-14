"""latest.price 001: one slot's price and the named parts it divides into,
proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.enums.price_component_name import PriceComponentName
from sema.runtime.types.latest_price import LatestPrice
from sema.runtime.types.old_versions.latest_price_000 import LatestPrice000
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("latest.price", "001")


def component(name: str, price_x1000: int) -> dict:
    return {
        "Name": name,
        "PriceX1000": price_x1000,
        "TypeName": "price.component",
        "Version": "000",
    }


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("latest.price", "001") == {1: ["a", "b"], 2: [], 3: ["a", "b"]}


def test_example_round_trips() -> None:
    price = LatestPrice.model_validate(EXAMPLE)
    assert sum(c.price_x1000 for c in price.components) == price.price_x1000
    assert LatestPrice.model_validate(price.model_dump(by_alias=True)) == price


def test_two_unknown_components_are_valid() -> None:
    def mutate(p: dict) -> None:
        p["Components"] = [component("Unknown", 100000), component("Unknown", 2360)]
        p["PriceX1000"] = 102360
        del p["TariffAlias"]

    LatestPrice.model_validate(mutated(EXAMPLE, mutate))


def test_a_name_from_a_later_enum_version_decodes_to_unknown_and_still_sums() -> None:
    def mutate(p: dict) -> None:
        p["Components"].append(component("RegulationAdder", 500))
        p["PriceX1000"] += 500

    price = LatestPrice.model_validate(mutated(EXAMPLE, mutate))
    assert price.components[-1].name == PriceComponentName.Unknown


def test_axiom_1a_refuses_no_components() -> None:
    def mutate(p: dict) -> None:
        p["Components"] = []
        p["PriceX1000"] = 0
        del p["TariffAlias"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, "a")


def test_axiom_1b_refuses_components_that_do_not_sum_to_the_price() -> None:
    def mutate(p: dict) -> None:
        p["PriceX1000"] += 1

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, "b")


def test_axiom_2_refuses_a_named_component_twice() -> None:
    def mutate(p: dict) -> None:
        p["Components"].append(component("WholesaleLoss", 0))

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3a_refuses_delivery_without_a_tariff() -> None:
    def mutate(p: dict) -> None:
        del p["TariffAlias"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3, "a")


def test_axiom_3b_refuses_a_tariff_without_delivery() -> None:
    def mutate(p: dict) -> None:
        delivery = next(c for c in p["Components"] if c["Name"] == "Delivery")
        p["Components"].remove(delivery)
        p["PriceX1000"] -= delivery["PriceX1000"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3, "b")


def test_a_000_price_upgrades_to_one_unknown_component_with_the_whole_price() -> None:
    old = example("latest.price", "000")
    upgraded = LatestPrice000.model_validate(old).upgrade()
    assert upgraded.version == "001"
    assert upgraded.price_x1000 == old["PriceTimes1000"]
    assert [(c.name, c.price_x1000) for c in upgraded.components] == [
        (PriceComponentName.Unknown, old["PriceTimes1000"])
    ]
    assert upgraded.tariff_alias is None
    assert upgraded.created_ms is None
