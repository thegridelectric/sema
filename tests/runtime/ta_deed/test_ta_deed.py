"""ta.deed axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("ta.deed", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("ta.deed", "000") == {1: []}


def test_axiom_1_refuses_simulated_asset_in_world_universe() -> None:
    def mutate(p: dict) -> None:
        p["ValidationState"] = "ValidatedSimulatedAsset"
        p["TaAlias"] = "w.isone.me.versant.keene.simbeech.ta"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)
