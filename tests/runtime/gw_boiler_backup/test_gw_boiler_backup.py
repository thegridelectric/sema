"""gw.boiler.backup 000: the relays, the optional failsafe, their distinctness."""

import pytest
from pydantic import ValidationError

from sema.runtime.types.gw_boiler_backup import GwBoilerBackup


def boiler(failsafe: str, aquastat_ctrl: str) -> dict[str, object]:
    return {
        "FailsafeRelayName": failsafe,
        "AquastatCtrlRelayName": aquastat_ctrl,
        "InService": True,
        "TypeName": "gw.boiler.backup",
        "Version": "000",
    }


def test_two_relays_validate() -> None:
    b = GwBoilerBackup.model_validate(
        boiler("hp-failsafe-relay", "aquastat-ctrl-relay")
    )
    assert b.in_service


def test_axiom_1_one_relay_for_both_roles() -> None:
    with pytest.raises(ValidationError, match="(?i)axiom 1"):
        GwBoilerBackup.model_validate(boiler("hp-failsafe-relay", "hp-failsafe-relay"))


def test_no_failsafe_relay_validates() -> None:
    b = boiler("unused", "aquastat-ctrl-relay")
    del b["FailsafeRelayName"]
    assert GwBoilerBackup.model_validate(b).failsafe_relay_name is None
