"""i2c.dac.output.component.gt axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("i2c.dac.output.component.gt", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("i2c.dac.output.component.gt", "000") == {1: []}


def test_axiom_1_refuses_two_configs_on_one_output() -> None:
    def mutate(p: dict) -> None:
        p["ConfigList"].append(
            {
                "ChannelName": "primary-010v",
                "ActorName": "primary-010v",
                "DacChannel": "D",
                "TypeName": "dac.output.config",
                "Version": "000",
            }
        )

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)
