import json
from pathlib import Path

import pytest

from sema.runtime.base import SemaError
from sema.runtime.codec import default_codec
from sema.runtime.types.gw_operational_params import GwOperationalParams


def test_default_v000_loads_as_gw_operational_params() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v000" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, GwOperationalParams)
    assert decoded.type_name == "gw.operational.params"
    assert decoded.version == "000"
    assert decoded.standby is False


def test_axiom_6_catches_a_standby_house0_loop_not_at_full_send() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v000" / "axiom_6.json"
    payload = json.loads(fixture.read_text())

    with pytest.raises(SemaError, match="(?i)Axiom 6"):
        default_codec.from_dict(payload)
