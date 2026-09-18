import json
import re
from pathlib import Path

import pytest

from sema.runtime.base import SemaError
from sema.runtime.codec import default_codec
from sema.runtime.types.sim_pico_btu_meter_component_gt import SimPicoBtuMeterComponentGt


def _axiom_match(n: int) -> re.Pattern[str]:
    return re.compile(rf"axiom {n}", re.IGNORECASE)


def _load_fixture(name: str) -> dict:
    fixture = Path(__file__).parent / "fixtures" / "v000" / name
    return json.loads(fixture.read_text())


def test_default_loads() -> None:
    decoded = default_codec.from_dict(_load_fixture("default.json"))

    assert isinstance(decoded, SimPicoBtuMeterComponentGt)
    assert decoded.read_ct_voltage is False


def test_ct_on_loads() -> None:
    decoded = default_codec.from_dict(_load_fixture("ct_on.json"))

    assert isinstance(decoded, SimPicoBtuMeterComponentGt)
    assert decoded.read_ct_voltage is True


@pytest.mark.parametrize("n", [1, 2])
def test_axiom_counterexample_is_rejected(n: int) -> None:
    with pytest.raises(SemaError, match=_axiom_match(n)):
        default_codec.from_dict(_load_fixture(f"axiom_{n}.json"))
