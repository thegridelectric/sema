"""i2c.dac.capability axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("i2c.dac.capability", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("i2c.dac.capability", "000") == {1: []}


def test_axiom_1_refuses_mux_name_without_mux_channel() -> None:
    def mutate(p: dict) -> None:
        p["MuxName"] = "DacMux"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)
