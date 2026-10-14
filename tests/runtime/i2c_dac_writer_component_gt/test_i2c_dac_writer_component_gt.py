"""i2c.dac.writer.component.gt axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("i2c.dac.writer.component.gt", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("i2c.dac.writer.component.gt", "000") == {1: []}


def test_axiom_1_refuses_duplicate_dac_channel() -> None:
    def mutate(p: dict) -> None:
        p["ConfigList"].append({**p["ConfigList"][0], "PowerOnRawValue": 0})

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)
