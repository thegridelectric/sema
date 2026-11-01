"""flo.recommendation 000: the bid curve and its paths, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.flo_recommendation import FloRecommendation
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("flo.recommendation", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.recommendation", "000") == {
        1: [],
        2: [],
        3: [],
        4: ["a", "b"],
        5: [],
    }


def test_example_round_trips() -> None:
    r = FloRecommendation.model_validate(EXAMPLE)
    assert [p.quantity_x1000 for p in r.pq_pairs] == [0, 4200]
    assert FloRecommendation.model_validate(r.model_dump(by_alias=True)) == r


def test_one_pair_one_path_is_valid() -> None:
    def mutate(p: dict) -> None:
        p["PqPairs"] = p["PqPairs"][:1]
        p["OptimalPathList"] = p["OptimalPathList"][:1]

    FloRecommendation.model_validate(mutated(EXAMPLE, mutate))


def test_axiom_1_refuses_no_pairs() -> None:
    def mutate(p: dict) -> None:
        p["PqPairs"] = []
        p["OptimalPathList"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_a_missing_path() -> None:
    def mutate(p: dict) -> None:
        p["OptimalPathList"] = p["OptimalPathList"][:1]

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
