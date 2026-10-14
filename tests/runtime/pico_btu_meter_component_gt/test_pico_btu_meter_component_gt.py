import json
from pathlib import Path

from sema.runtime.codec import default_codec
from sema.runtime.types.pico_btu_meter_component_gt import PicoBtuMeterComponentGt
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("pico.btu.meter.component.gt", "000")


def _load_fixture(name: str) -> dict:
    fixture = Path(__file__).parent / "fixtures" / "v000" / name
    return json.loads(fixture.read_text())


def test_default_loads() -> None:
    decoded = default_codec.from_dict(_load_fixture("default.json"))

    assert isinstance(decoded, PicoBtuMeterComponentGt)
    assert decoded.read_ct_voltage is False


def test_ct_on_loads() -> None:
    decoded = default_codec.from_dict(_load_fixture("ct_on.json"))

    assert isinstance(decoded, PicoBtuMeterComponentGt)
    assert decoded.read_ct_voltage is True


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("pico.btu.meter.component.gt", "000") == {1: [], 2: []}


def test_axiom_1_refuses_read_ct_voltage_without_ct_volts_delta() -> None:
    def mutate(p: dict) -> None:
        p["ReadCtVoltage"] = True
        p["CtChannelName"] = "hp-ct-volts"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_read_ct_voltage_without_ct_channel_name() -> None:
    def mutate(p: dict) -> None:
        p["ReadCtVoltage"] = True
        p["AsyncCaptureDeltaCtVoltsX100"] = 50

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)
