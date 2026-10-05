import json
from pathlib import Path

import pytest

from sema.runtime.base import SemaError
from sema.runtime.codec import default_codec
from sema.runtime.types.gw_recorded_setpoints import GwRecordedSetpoints


def test_default_v000_loads_as_gw_recorded_setpoints() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v000" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, GwRecordedSetpoints)
    assert decoded.type_name == "gw.recorded.setpoints"
    assert decoded.version == "000"
    assert decoded.setpoint_list[0].channel_name == "zone1-bedrooms-set"


def test_axiom_1_catches_a_channel_recorded_twice() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v000" / "axiom_1.json"
    payload = json.loads(fixture.read_text())

    with pytest.raises(SemaError, match="(?i)Axiom 1"):
        default_codec.from_dict(payload)
