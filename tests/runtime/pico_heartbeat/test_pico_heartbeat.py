import pytest

from sema.runtime.base import SemaError
from sema.runtime.codec import default_codec
from sema.runtime.enums.pico_reset_cause import PicoResetCause
from sema.runtime.types.pico_heartbeat import PicoHeartbeat
from tests.runtime.refusal import example

EXAMPLE_000 = example("pico.heartbeat", "000")


def test_example_decodes() -> None:
    decoded = default_codec.from_dict(EXAMPLE_000, auto_upgrade=False)
    assert isinstance(decoded, PicoHeartbeat)
    assert decoded.reset_cause == PicoResetCause.PowerOn
    assert decoded.uptime_s == 3


def test_negative_uptime_is_refused() -> None:
    with pytest.raises((SemaError, ValueError)):
        default_codec.from_dict(dict(EXAMPLE_000, UptimeS=-1), auto_upgrade=False)


def test_unknown_reset_cause_decodes_to_unknown() -> None:
    """A cause appended in a later enum version reaches this decoder as Unknown."""
    decoded = default_codec.from_dict(
        dict(EXAMPLE_000, ResetCause="Brownout"), auto_upgrade=False
    )
    assert isinstance(decoded, PicoHeartbeat)
    assert decoded.reset_cause == PicoResetCause.Unknown
