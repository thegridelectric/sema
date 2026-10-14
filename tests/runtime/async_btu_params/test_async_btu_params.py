import json
from pathlib import Path

import pytest

from sema.runtime.base import UpgradeRequiresContext
from sema.runtime.codec import default_codec
from sema.runtime.enums.pico_board_variant import PicoBoardVariant
from sema.runtime.types.async_btu_params import AsyncBtuParams
from sema.runtime.types.old_versions.async_btu_params_000 import AsyncBtuParams000
from sema.runtime.types.old_versions.async_btu_params_100 import AsyncBtuParams100
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE_000 = example("async.btu.params", "000")
EXAMPLE_100 = example("async.btu.params", "100")
EXAMPLE_110 = example("async.btu.params", "110")


def _load_fixture(name: str, version_dir: str) -> dict:
    fixture = Path(__file__).parent / "fixtures" / version_dir / name
    return json.loads(fixture.read_text())


def test_async_btu_params_latest_version_is_110() -> None:
    assert AsyncBtuParams.version_value() == "110"


def test_v000_wire_shape_decodes() -> None:
    """The shipped 000 wire shape, null CtChannelName and float CaptureOffsetS included."""
    decoded = default_codec.from_dict(
        _load_fixture("default.json", "v000"), auto_upgrade=False
    )

    assert isinstance(decoded, AsyncBtuParams000)
    assert decoded.ct_channel_name is None
    assert decoded.capture_offset_s == 41.5


def test_v000_does_not_upgrade_without_context() -> None:
    """A 000 message cannot know its board; the upgrade refuses rather than guesses."""
    decoded = default_codec.from_dict(
        _load_fixture("default.json", "v000"), auto_upgrade=False
    )
    assert isinstance(decoded, AsyncBtuParams000)

    with pytest.raises(UpgradeRequiresContext):
        decoded.upgrade()

    with pytest.raises(UpgradeRequiresContext):
        default_codec.from_dict(_load_fixture("default.json", "v000"))


def test_v100_wire_shape_decodes() -> None:
    """The 100 wire shape, board and MicroPython release included."""
    decoded = default_codec.from_dict(
        _load_fixture("default.json", "v100"), auto_upgrade=False
    )

    assert isinstance(decoded, AsyncBtuParams100)
    assert decoded.pico_board_variant == PicoBoardVariant.PicoRaspberryWifi2040
    assert decoded.micropython_version == "1.24.1"


def test_v100_does_not_upgrade_without_context() -> None:
    """A 100 message cannot know its firmware commit; the upgrade refuses rather than guesses."""
    decoded = default_codec.from_dict(
        _load_fixture("default.json", "v100"), auto_upgrade=False
    )
    assert isinstance(decoded, AsyncBtuParams100)

    with pytest.raises(UpgradeRequiresContext):
        decoded.upgrade()

    with pytest.raises(UpgradeRequiresContext):
        default_codec.from_dict(_load_fixture("default.json", "v100"))


def test_v110_default_loads() -> None:
    decoded = default_codec.from_dict(_load_fixture("default.json", "v110"))

    assert isinstance(decoded, AsyncBtuParams)
    assert decoded.pico_board_variant == PicoBoardVariant.PicoRaspberryWifi2040
    assert decoded.micropython_version == "1.24.1"
    assert decoded.firmware_commit == "9f4c1d2e7a8b0c3d5e6f70819a2b3c4d5e6f7081"
    assert decoded.capture_offset_s is None


def test_v110_unknown_board_coerces_to_unknown() -> None:
    """An out-of-vocabulary board value lands on Unknown, never on a real board."""
    raw = _load_fixture("default.json", "v110")
    raw["PicoBoardVariant"] = "Esp32Something"
    decoded = default_codec.from_dict(raw)

    assert isinstance(decoded, AsyncBtuParams)
    assert decoded.pico_board_variant == PicoBoardVariant.Unknown


def test_v000_every_axiom_has_a_mutation() -> None:
    assert axioms("async.btu.params", "000") == {1: []}


def test_v000_axiom_1_refuses_read_ct_voltage_without_ct_channel_name() -> None:
    def mutate(p: dict) -> None:
        p["ReadCtVoltage"] = True

    assert_refused(default_codec, mutated(EXAMPLE_000, mutate), 1)


def test_v100_every_axiom_has_a_mutation() -> None:
    assert axioms("async.btu.params", "100") == {1: []}


def test_v100_axiom_1_refuses_read_ct_voltage_without_ct_channel_name() -> None:
    def mutate(p: dict) -> None:
        p["ReadCtVoltage"] = True

    assert_refused(default_codec, mutated(EXAMPLE_100, mutate), 1)


def test_v110_every_axiom_has_a_mutation() -> None:
    assert axioms("async.btu.params", "110") == {1: []}


def test_v110_axiom_1_refuses_read_ct_voltage_without_ct_channel_name() -> None:
    def mutate(p: dict) -> None:
        p["ReadCtVoltage"] = True

    assert_refused(default_codec, mutated(EXAMPLE_110, mutate), 1)
