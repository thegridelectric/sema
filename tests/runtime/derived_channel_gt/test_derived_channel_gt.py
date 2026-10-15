import json
from pathlib import Path

from sema.runtime.codec import default_codec
from sema.runtime.types.derived_channel_gt import DerivedChannelGt
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("derived.channel.gt", "003")


def test_derived_channel_gt_latest_version_is_003() -> None:
    assert DerivedChannelGt.version_value() == "003"


def test_default_v000_upgrades_to_latest() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v000" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, DerivedChannelGt)
    assert decoded.type_name == "derived.channel.gt"
    assert decoded.version == "003"


def test_default_v001_upgrades_to_latest() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v001" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, DerivedChannelGt)
    assert decoded.type_name == "derived.channel.gt"
    assert decoded.version == "003"


def test_default_v002_upgrades_to_latest() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v002" / "default.json"
    payload = json.loads(fixture.read_text())
    decoded = default_codec.from_dict(payload)
    assert isinstance(decoded, DerivedChannelGt)
    assert decoded.type_name == "derived.channel.gt"
    assert decoded.version == "003"


def test_default_v003_loads_as_derived_channel_gt() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v003" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, DerivedChannelGt)
    assert decoded.type_name == "derived.channel.gt"
    assert decoded.version == "003"


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("derived.channel.gt", "003") == {1: [], 2: [], 3: [], 4: []}


def test_axiom_1_refuses_periodic_without_emit_period() -> None:
    def mutate(p: dict) -> None:
        del p["EmitPeriodS"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_output_quantity_not_matching_unit() -> None:
    def mutate(p: dict) -> None:
        p["OutputQuantity"] = "Power"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_3_refuses_affine_without_calibration() -> None:
    def mutate(p: dict) -> None:
        p["Strategy"] = "affine"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_axiom_4_refuses_system_model_without_energy_model() -> None:
    def mutate(p: dict) -> None:
        del p["Parameters"]["EnergyModel"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)
