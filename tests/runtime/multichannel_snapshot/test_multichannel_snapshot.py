from sema.runtime.codec import default_codec
from sema.runtime.enums.spaceheat_telemetry_name import SpaceheatTelemetryName
from sema.runtime.types.multichannel_snapshot import MultichannelSnapshot
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE_000 = example("multichannel.snapshot", "000")


def test_latest_version_is_000() -> None:
    assert MultichannelSnapshot.version_value() == "000"


def test_shipped_wire_shape_decodes() -> None:
    """The shape the fleet btu meter posts."""
    decoded = default_codec.from_dict(EXAMPLE_000, auto_upgrade=False)
    assert isinstance(decoded, MultichannelSnapshot)
    assert decoded.unit_list == [
        SpaceheatTelemetryName.GpmTimes100,
        SpaceheatTelemetryName.CelsiusTimes100,
        SpaceheatTelemetryName.CelsiusTimes100,
    ]


def test_v000_every_axiom_has_a_mutation() -> None:
    assert axioms("multichannel.snapshot", "000") == {1: []}


def test_v000_axiom_1_refuses_unequal_lists() -> None:
    def mutate(p: dict) -> None:
        p["UnitList"] = p["UnitList"][:-1]

    assert_refused(default_codec, mutated(EXAMPLE_000, mutate), 1)
