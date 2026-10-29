import json
from pathlib import Path

import pytest

from sema.runtime.base import SemaError
from sema.runtime.codec import default_codec
from sema.runtime.enums.gw_dashboard_role import GwDashboardRole
from sema.runtime.types.gw_house_operating_status import GwHouseOperatingStatus
from sema.runtime.types.gw_house_summary import GwHouseSummary
from sema.runtime.types.old_versions.gw_house_summary_000 import GwHouseSummary000


def load_fixture(name: str, version_dir: str) -> dict:
    fixture = Path(__file__).parent / "fixtures" / version_dir / name
    return json.loads(fixture.read_text())


def operating_status() -> dict:
    return {
        "ScadaAlias": "hw1.isone.me.versant.keene.beech.scada",
        "ValidationState": "ValidatedRealAssetAndGps",
        "Standby": False,
        "StandbyPosture": "NoHeatingOrCooling",
        "SeasonalStorageMode": "AllTanks",
        "ServiceMode": "Heating",
        "AcceptsDispatch": True,
        "TopState": "Auto",
        "ScadaBlind": False,
        "LtnDispatching": False,
        "CreatedMs": 1792013000000,
        "TypeName": "gw.house.operating.status",
        "Version": "000",
    }


def test_latest_version_is_001() -> None:
    assert GwHouseSummary.version_value() == "001"


def test_v001_loads_with_scada_commit() -> None:
    decoded = default_codec.from_dict(load_fixture("default.json", "v001"))

    assert isinstance(decoded, GwHouseSummary)
    assert decoded.role is GwDashboardRole.Admin
    assert decoded.scada_commit == "e55faa2d3b1c4f6a8d9e0f1a2b3c4d5e6f7a8b9c"


def test_v001_scada_commit_takes_the_dirty_suffix_and_refuses_a_short_hash() -> None:
    raw = load_fixture("default.json", "v001")
    raw["ScadaCommit"] = raw["ScadaCommit"] + "-dirty"
    decoded = default_codec.from_dict(raw)
    assert isinstance(decoded, GwHouseSummary)
    assert decoded.scada_commit is not None
    assert decoded.scada_commit.endswith("-dirty")

    raw["ScadaCommit"] = "e55faa2d"
    with pytest.raises(SemaError):
        default_codec.from_dict(raw)


def test_v000_minimal_loads_and_upgrades() -> None:
    decoded = default_codec.from_dict(load_fixture("default.json", "v000"), auto_upgrade=False)
    assert isinstance(decoded, GwHouseSummary000)

    upgraded = decoded.upgrade()
    assert isinstance(upgraded, GwHouseSummary)
    assert upgraded.role is GwDashboardRole.Viewer
    assert upgraded.layout is None
    assert upgraded.operating_status is None
    assert upgraded.longest_running_zone_name is None
    assert upgraded.scada_commit is None


def test_nested_operating_status_decodes() -> None:
    raw = load_fixture("default.json", "v000")
    raw["OperatingStatus"] = operating_status()
    decoded = default_codec.from_dict(raw)

    assert isinstance(decoded, GwHouseSummary)
    assert isinstance(decoded.operating_status, GwHouseOperatingStatus)
    assert decoded.operating_status.created_ms == 1792013000000


def test_zone_pair_together_loads() -> None:
    raw = load_fixture("default.json", "v000")
    raw["LongestRunningZoneName"] = "zone1-downstairs"
    raw["LongestRunningZoneStartTime"] = "2026-10-21T15:00:00Z"
    decoded = default_codec.from_dict(raw)
    assert isinstance(decoded, GwHouseSummary)
    assert decoded.longest_running_zone_name == "zone1-downstairs"


def test_axiom_1_zone_name_without_start_time_refused() -> None:
    raw = load_fixture("default.json", "v000")
    raw["LongestRunningZoneName"] = "zone1-downstairs"
    with pytest.raises(SemaError, match="(?i)axiom 1"):
        default_codec.from_dict(raw)


def test_axiom_1_start_time_without_zone_name_refused() -> None:
    raw = load_fixture("default.json", "v000")
    raw["LongestRunningZoneStartTime"] = "2026-10-21T15:00:00Z"
    with pytest.raises(SemaError, match="(?i)axiom 1"):
        default_codec.from_dict(raw)


def test_unknown_role_decodes_to_viewer() -> None:
    raw = load_fixture("default.json", "v000")
    raw["Role"] = "Installer"
    decoded = default_codec.from_dict(raw)
    assert isinstance(decoded, GwHouseSummary)
    assert decoded.role is GwDashboardRole.Viewer


def test_ta_g_node_id_is_uuid4() -> None:
    raw = load_fixture("default.json", "v000")
    raw["TaGNodeId"] = "beech"
    with pytest.raises(SemaError):
        default_codec.from_dict(raw)
