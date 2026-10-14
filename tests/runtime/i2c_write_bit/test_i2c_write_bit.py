"""i2c.write.bit axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("i2c.write.bit", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("i2c.write.bit", "000") == {1: []}


def test_axiom_1_refuses_bit_value_out_of_range() -> None:
    def mutate(p: dict) -> None:
        p["Value"] = 2

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)
