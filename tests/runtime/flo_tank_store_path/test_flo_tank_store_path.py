"""flo.tank.store.path 000: the layered store along a path, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.flo_tank_store_path import FloTankStorePath
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("flo.tank.store.path", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.tank.store.path", "000") == {1: [], 2: [], 3: []}


def test_example_round_trips() -> None:
    r = FloTankStorePath.model_validate(EXAMPLE)
    assert r.thermocline1_list == [8, 6, 8]
    assert FloTankStorePath.model_validate(r.model_dump(by_alias=True)) == r


def test_two_bands_set_both_thermoclines_equal() -> None:
    def mutate(p: dict) -> None:
        p["Thermocline2List"] = p["Thermocline1List"]

    FloTankStorePath.model_validate(mutated(EXAMPLE, mutate))


def test_axiom_1_refuses_a_short_list() -> None:
    def mutate(p: dict) -> None:
        p["BottomFList"] = [100, 100]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_thermoclines_out_of_order() -> None:
    def mutate(p: dict) -> None:
        p["Thermocline1List"][1] = p["Thermocline2List"][1] + 1

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_2_refuses_a_thermocline_below_the_store() -> None:
    def mutate(p: dict) -> None:
        p["Thermocline2List"][2] = p["StoreLayers"] + 1

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_an_empty_store_at_the_full_energy() -> None:
    def mutate(p: dict) -> None:
        p["EmptyStoreWh"] = p["FullStoreWh"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)
