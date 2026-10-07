"""gw.weather.seasonal.template.gt axiom counterexamples — sema must reject
what violates an axiom."""

import json
from pathlib import Path

import pytest

from sema.runtime.base import SemaError
from sema.runtime.codec import default_codec

FIX = Path(__file__).parent / "fixtures" / "v000"


def _rejects(fixture: str, axiom: str) -> None:
    payload = json.loads((FIX / fixture).read_text())
    with pytest.raises(SemaError, match=f"(?i)axiom {axiom}"):
        default_codec.from_dict(payload)


def test_axiom_1_catches_eleven_months() -> None:
    _rejects("axiom_1.json", "1")
