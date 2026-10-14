from sema.runtime.codec import default_codec
from sema.runtime.types.microvolts import Microvolts
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE_100 = example("microvolts", "100")


def test_latest_version_is_100() -> None:
    assert Microvolts.version_value() == "100"


def test_shipped_wire_shape_decodes() -> None:
    """The shape the fleet tank module posts."""
    decoded = default_codec.from_dict(EXAMPLE_100, auto_upgrade=False)
    assert isinstance(decoded, Microvolts)
    assert decoded.micro_volts_list == [1792211, 1811450, 1830102]


def test_v100_every_axiom_has_a_mutation() -> None:
    assert axioms("microvolts", "100") == {1: []}


def test_v100_axiom_1_refuses_unequal_lists() -> None:
    def mutate(p: dict) -> None:
        p["MicroVoltsList"].append(0)

    assert_refused(default_codec, mutated(EXAMPLE_100, mutate), 1)
