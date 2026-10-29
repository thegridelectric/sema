"""gw.command.interface axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.command.interface", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.command.interface", "000") == {1: [], 2: [], 3: []}


def test_axiom_1_refuses_empty_commands() -> None:
    def mutate(p: dict) -> None:
        p["Commands"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_event_outside_event_type_vocabulary() -> None:
    def mutate(p: dict) -> None:
        p["Commands"][0]["Event"] = "TurnSideways"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_state_outside_state_type_vocabulary() -> None:
    def mutate(p: dict) -> None:
        p["Commands"][0]["ToState"] = "HpSideways"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


EXAMPLE_001 = example("gw.command.interface", "001")


def test_001_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.command.interface", "001") == {1: [], 2: [], 3: []}


def test_001_axiom_1_refuses_empty_commands() -> None:
    def mutate(p: dict) -> None:
        p["Commands"] = []

    assert_refused(default_codec, mutated(EXAMPLE_001, mutate), 1)


def test_001_axiom_2_refuses_event_outside_event_type_vocabulary() -> None:
    def mutate(p: dict) -> None:
        p["Commands"][0]["Event"] = "TurnSideways"

    assert_refused(default_codec, mutated(EXAMPLE_001, mutate), 2)


def test_001_axiom_3_refuses_state_outside_state_type_vocabulary() -> None:
    def mutate(p: dict) -> None:
        p["Commands"][0]["ToState"] = "HpSideways"

    assert_refused(default_codec, mutated(EXAMPLE_001, mutate), 3)
