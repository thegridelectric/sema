"""zero.ten.power.on axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("zero.ten.power.on", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("zero.ten.power.on", "000") == {1: []}


def test_axiom_1_refuses_level_above_ten_volts() -> None:
    def mutate(p: dict) -> None:
        p["PowerOnVoltsTimesTen"] = 101

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)
