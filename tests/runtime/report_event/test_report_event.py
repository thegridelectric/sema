import json
from pathlib import Path

from sema.runtime.codec import default_codec
from sema.runtime.types.report_event import ReportEvent


def test_report_event_latest_version_is_004() -> None:
    assert ReportEvent.version_value() == "004"


def test_default_v002_upgrades_to_latest() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v002" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, ReportEvent)
    assert decoded.type_name == "report.event"
    assert decoded.version == "004"


def test_default_v003_upgrades_to_latest() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v003" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, ReportEvent)
    assert decoded.type_name == "report.event"
    assert decoded.version == "004"


def test_default_v004_loads_as_report_event() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v004" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, ReportEvent)
    assert decoded.type_name == "report.event"
    assert decoded.version == "004"


def test_live_v003_upgrades_by_propagating_report_identity() -> None:
    """A field 003 whose MessageId and TimeCreatedMs differ from the report's
    (spruce, 2026-10-17) upgrades to 004 by taking the report's own id and
    created time, which is what the reinstated axioms mean."""
    fixture = Path(__file__).parent / "fixtures" / "v003" / "spruce-2026-10-17.json"
    payload = json.loads(fixture.read_text())
    assert payload["MessageId"] != payload["Report"]["Id"]
    assert payload["TimeCreatedMs"] != payload["Report"]["MessageCreatedMs"]

    as_sent = default_codec.from_dict(payload, auto_upgrade=False)
    assert as_sent.version == "003"

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, ReportEvent)
    assert decoded.version == "004"
    assert decoded.message_id == decoded.report.id
    assert decoded.time_created_ms == decoded.report.message_created_ms
    assert decoded.src == decoded.report.from_g_node_alias
