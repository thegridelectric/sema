"""layout.bundle axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("layout.bundle", "000")
LAYOUT_LITE_012 = example("layout.lite", "012")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("layout.bundle", "000") == {1: []}


def test_a_bundle_of_distinct_senders_decodes() -> None:
    def mutate(p: dict) -> None:
        p["Layouts"] = [LAYOUT_LITE_012]

    decoded = default_codec.from_dict(mutated(EXAMPLE, mutate))
    assert decoded.type_name == "layout.bundle"
    assert len(decoded.layouts) == 1


def test_axiom_1_refuses_a_repeated_sender() -> None:
    def mutate(p: dict) -> None:
        p["Layouts"] = [LAYOUT_LITE_012, LAYOUT_LITE_012]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)
