"""flo.recommendation 001: the bid curve, its paths and their store-state and
penalty annotations, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.flo_recommendation import FloRecommendation
from sema.runtime.types.old_versions.flo_recommendation_000 import FloRecommendation000
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("flo.recommendation", "001")
ANNOTATIONS = ("OptimalPathList", "StoreStateList", "PathPenaltiesList")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.recommendation", "001") == {
        1: [],
        2: [],
        3: [],
        4: ["a", "b"],
        5: [],
        6: [],
        7: [],
    }


def test_example_round_trips() -> None:
    r = FloRecommendation.model_validate(EXAMPLE)
    assert [p.quantity_x1000 for p in r.pq_pairs] == [0, 4200]
    assert FloRecommendation.model_validate(r.model_dump(by_alias=True)) == r


def test_one_pair_one_path_is_valid() -> None:
    def mutate(p: dict) -> None:
        p["PqPairs"] = p["PqPairs"][:1]
        for name in ANNOTATIONS:
            p[name] = p[name][:1]

    FloRecommendation.model_validate(mutated(EXAMPLE, mutate))


def test_bare_paths_are_valid() -> None:
    def mutate(p: dict) -> None:
        del p["StoreStateList"]
        del p["PathPenaltiesList"]

    r = FloRecommendation.model_validate(mutated(EXAMPLE, mutate))
    assert r.store_state_list is None and r.path_penalties_list is None


def test_axiom_1_refuses_no_pairs() -> None:
    def mutate(p: dict) -> None:
        p["PqPairs"] = []
        for name in ANNOTATIONS:
            p[name] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_a_missing_path() -> None:
    def mutate(p: dict) -> None:
        for name in ANNOTATIONS:
            p[name] = p[name][:1]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_a_path_whose_first_step_is_not_the_bid() -> None:
    def mutate(p: dict) -> None:
        p["OptimalPathList"][1]["HpAvgWList"][0] = 4199

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_3_scales_avg_mw_to_watts() -> None:
    def mutate(p: dict) -> None:
        p["QuantityUnit"] = "AvgMW"
        p["PqPairs"][1]["QuantityX1000"] = 4
        p["OptimalPathList"][1]["HpAvgWList"][0] = 4000

    FloRecommendation.model_validate(mutated(EXAMPLE, mutate))


def test_axiom_4_a_refuses_ascending_prices() -> None:
    def mutate(p: dict) -> None:
        p["PqPairs"][1]["PriceX1000"] = 2000000

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, "a")


def test_axiom_4_b_refuses_a_falling_quantity() -> None:
    def mutate(p: dict) -> None:
        p["PqPairs"][0]["QuantityX1000"] = 5000
        p["OptimalPathList"][0]["HpAvgWList"][0] = 5000

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, "b")


def test_axiom_5_refuses_paths_that_start_apart() -> None:
    def mutate(p: dict) -> None:
        p["OptimalPathList"][0]["StartUnixS"] = 1762012800

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 5)


def test_axiom_6_refuses_a_missing_store_state_word() -> None:
    def mutate(p: dict) -> None:
        p["StoreStateList"] = p["StoreStateList"][:1]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 6)


def test_axiom_6_refuses_store_state_with_another_step_count() -> None:
    def mutate(p: dict) -> None:
        store = p["StoreStateList"][0]
        for name in (
            "TopFList",
            "MiddleFList",
            "BottomFList",
            "Thermocline1List",
            "Thermocline2List",
        ):
            store[name] = store[name][:2]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 6)


def test_axiom_7_refuses_a_missing_penalties_word() -> None:
    def mutate(p: dict) -> None:
        p["PathPenaltiesList"] = p["PathPenaltiesList"][:1]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 7)


def test_axiom_7_refuses_penalties_with_another_step_count() -> None:
    def mutate(p: dict) -> None:
        penalties = p["PathPenaltiesList"][0]
        for name in (
            "RswtPenaltyUsdList",
            "StabilityPenaltyUsdList",
            "ShortCyclePenaltyUsdList",
        ):
            penalties[name] = [0.0, 0.0]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 7)


def test_a_000_recommendation_upgrades_bare() -> None:
    old = example("flo.recommendation", "000")
    upgraded = FloRecommendation000.model_validate(old).upgrade()
    assert upgraded.version == "001"
    assert [p.version for p in upgraded.optimal_path_list] == ["000", "000"]
    assert upgraded.store_state_list is None and upgraded.path_penalties_list is None
