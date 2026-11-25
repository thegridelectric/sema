"""ta.deed axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.ta_deed import TaDeed
from tests.runtime.refusal import (
    assert_refused,
    axioms,
    example,
    mutated,
    runtime_class,
)

EXAMPLE = example("ta.deed", "001")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("ta.deed", "001") == {1: [], 2: []}


def test_axiom_1_refuses_simulated_asset_in_world_universe() -> None:
    def mutate(p: dict) -> None:
        p["ValidationState"] = "ValidatedSimulatedAsset"
        p["TaAlias"] = "w.isone.me.versant.keene.simbeech.ta"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_real_asset_in_d_universe() -> None:
    def mutate(p: dict) -> None:
        p["ValidationState"] = "ValidatedRealAssetAndGps"
        p["TaAlias"] = "d1.isone.me.versant.keene.beech.ta"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_v000_upgrades_to_v001() -> None:
    old = runtime_class("ta.deed", "000")
    payload = dict(example("ta.deed", "000"))
    upgraded = old.model_validate(payload).upgrade()
    assert isinstance(upgraded, TaDeed)
    assert upgraded.version == "001"
    assert upgraded.ta_alias == payload["TaAlias"]
