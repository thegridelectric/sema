"""gw.weather.seasonal.template.gt axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.weather.seasonal.template.gt", "000")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.weather.seasonal.template.gt", "000") == {1: []}


def test_axiom_1_refuses_eleven_months() -> None:
    def mutate(p: dict) -> None:
        p["TempByMonth"] = p["TempByMonth"][:11]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)
