"""i2c.write.reg axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("i2c.write.reg", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("i2c.write.reg", "000") == {1: [], 2: []}


def test_axiom_1_refuses_num_bytes_out_of_range() -> None:
    def mutate(p: dict) -> None:
        p["NumBytes"] = 3

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_value_too_big_for_num_bytes() -> None:
    def mutate(p: dict) -> None:
        p["NumBytes"] = 1

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)
