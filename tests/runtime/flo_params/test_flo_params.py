"""flo.params 000: one request to a FLO, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.flo_params import FloParams
from sema.runtime.types.flo_tuning_alice import FloTuningAlice
from sema.runtime.types.flo_tuning_bruce import FloTuningBruce
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("flo.params", "000")
PATH = example("flo.optimal.path", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.params", "000") == {1: [], 2: [], 3: [], 4: [], 5: []}


def test_example_round_trips_with_bruce_tuning() -> None:
    r = FloParams.model_validate(EXAMPLE)
    assert isinstance(r.tuning, FloTuningBruce)
    assert r.tuning.hp_constant_lift_f == 20
    assert FloParams.model_validate(r.model_dump(by_alias=True)) == r


def test_alice_tuning_selects_alice() -> None:
    def mutate(p: dict) -> None:
        p["Tuning"] = example("flo.tuning.alice", "000")

    r = FloParams.model_validate(mutated(EXAMPLE, mutate))
    assert isinstance(r.tuning, FloTuningAlice)


def test_previous_run_present_validates() -> None:
    def mutate(p: dict) -> None:
        p["PreviousOptimalPath"] = PATH
        p["PreviousEstimateElecUsdMwhNow"] = 78.3

    FloParams.model_validate(mutated(EXAMPLE, mutate))


def test_all_tanks_three_tanks_validates() -> None:
    def mutate(p: dict) -> None:
        p["SeasonalStorageMode"] = "AllTanks"
        p["TanksModeled"] = 3
        p["InitialThermocline1"] = 4
        p["InitialThermocline2"] = 9

    FloParams.model_validate(mutated(EXAMPLE, mutate))


def test_axiom_1_refuses_a_short_forecast() -> None:
    def mutate(p: dict) -> None:
        p["OatFList"] = p["OatFList"][:2]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_a_thermocline_below_the_store() -> None:
    def mutate(p: dict) -> None:
        p["InitialThermocline2"] = 4

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_buffer_only_with_three_tanks() -> None:
    def mutate(p: dict) -> None:
        p["TanksModeled"] = 3

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_refuses_a_floor_above_the_ceiling() -> None:
    def mutate(p: dict) -> None:
        p["PriceMinUsdMwh"] = 2500

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)


def test_axiom_5_refuses_a_lone_previous_path() -> None:
    def mutate(p: dict) -> None:
        p["PreviousOptimalPath"] = PATH

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 5)
