"""i2c.dac.channel.config axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("i2c.dac.channel.config", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("i2c.dac.channel.config", "000") == {1: ["a", "b"]}


def test_axiom_1_a_refuses_raw_value_beyond_12_bits() -> None:
    def mutate(p: dict) -> None:
        p["PowerOnRawValue"] = 4096

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, clause="a")


def test_axiom_1_b_refuses_gain_not_one_or_two() -> None:
    def mutate(p: dict) -> None:
        p["PowerOnGain"] = 3

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, clause="b")
