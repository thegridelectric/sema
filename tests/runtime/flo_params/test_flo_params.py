"""flo.params 002: one request to a FLO, proved by mutation of the example."""

import pytest

from sema.runtime.base import UpgradeRequiresContext
from sema.runtime.codec import default_codec
from sema.runtime.types.flo_params import FloParams
from sema.runtime.types.flo_tuning_alice import FloTuningAlice
from sema.runtime.types.flo_tuning_bruce import FloTuningBruce
from sema.runtime.types.old_versions.flo_params_000 import FloParams000
from sema.runtime.types.old_versions.flo_params_001 import FloParams001
from sema.runtime.types.old_versions.flo_tuning_bruce_000 import FloTuningBruce000
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("flo.params", "002")
PATH = example("flo.optimal.path", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.params", "002") == {1: [], 2: [], 3: [], 4: [], 5: []}


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


def test_a_000_request_upgrades_with_the_layers_it_modeled() -> None:
    old = example("flo.params", "000")
    upgraded = FloParams000.model_validate(old).upgrade()
    assert isinstance(upgraded.tuning, FloTuningBruce)
    assert upgraded.tuning.num_layers == old["TanksModeled"] * old["TempSensorsPerTank"]
    assert upgraded.version == "001"
    assert upgraded.tuning.version == "001"


def test_a_001_request_refuses_to_upgrade_for_want_of_its_price_forecast() -> None:
    old = example("flo.params", "001")
    with pytest.raises(UpgradeRequiresContext):
        FloParams001.model_validate(old).upgrade()


def test_a_request_without_its_price_forecast_id_is_refused() -> None:
    def mutate(p: dict) -> None:
        del p["PriceForecastId"]

    with pytest.raises(ValueError, match="PriceForecastId"):
        FloParams.model_validate(mutated(EXAMPLE, mutate))


def test_a_000_tuning_alone_refuses_to_upgrade() -> None:
    old = example("flo.tuning.bruce", "000")
    with pytest.raises(UpgradeRequiresContext):
        FloTuningBruce000.model_validate(old).upgrade()
