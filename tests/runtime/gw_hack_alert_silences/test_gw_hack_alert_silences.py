import json
from pathlib import Path

import pytest

from sema.runtime.base import SemaError
from sema.runtime.codec import default_codec
from sema.runtime.types.gw_hack_alert_silences import GwHackAlertSilences


def load_fixture(name: str, version_dir: str) -> dict:
    fixture = Path(__file__).parent / "fixtures" / version_dir / name
    return json.loads(fixture.read_text())


def test_latest_version_is_000() -> None:
    assert GwHackAlertSilences.version_value() == "000"


def test_v000_default_loads() -> None:
    decoded = default_codec.from_dict(load_fixture("default.json", "v000"))

    assert isinstance(decoded, GwHackAlertSilences)
    assert decoded.src == "hw1.alerts"
    assert decoded.silenced_g_node_aliases == ["hw1.isone.me.versant.keene.elm.ta"]


def test_empty_list_is_valid() -> None:
    raw = load_fixture("default.json", "v000")
    raw["SilencedGNodeAliases"] = []
    decoded = default_codec.from_dict(raw)
    assert isinstance(decoded, GwHackAlertSilences)
    assert decoded.silenced_g_node_aliases == []


def test_axiom_1_alias_must_be_a_terminal_asset() -> None:
    raw = load_fixture("default.json", "v000")
    raw["SilencedGNodeAliases"] = ["hw1.isone.me.versant.keene.elm.scada"]
    with pytest.raises(SemaError, match="(?i)axiom 1"):
        default_codec.from_dict(raw)


def test_alias_is_left_right_dot() -> None:
    raw = load_fixture("default.json", "v000")
    raw["SilencedGNodeAliases"] = ["Elm.ta"]
    with pytest.raises(SemaError):
        default_codec.from_dict(raw)
