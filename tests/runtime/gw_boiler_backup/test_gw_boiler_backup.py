"""gw.boiler.backup: 001 with the optional failsafe, 000 requiring it, their distinctness."""

import pytest
from pydantic import ValidationError

from sema.runtime.types.gw_boiler_backup import GwBoilerBackup
from sema.runtime.types.old_versions.gw_boiler_backup_000 import GwBoilerBackup000


def boiler(
    failsafe: str, aquastat_ctrl: str, version: str = "001"
) -> dict[str, object]:
    return {
        "FailsafeRelayName": failsafe,
        "AquastatCtrlRelayName": aquastat_ctrl,
        "InService": True,
        "TypeName": "gw.boiler.backup",
        "Version": version,
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


def test_000_requires_the_failsafe_relay() -> None:
    b = boiler("unused", "aquastat-ctrl-relay", version="000")
    del b["FailsafeRelayName"]
    with pytest.raises(ValidationError, match="FailsafeRelayName"):
        GwBoilerBackup000.model_validate(b)


def test_000_axiom_1_one_relay_for_both_roles() -> None:
    with pytest.raises(ValidationError, match="(?i)axiom 1"):
        GwBoilerBackup000.model_validate(
            boiler("hp-failsafe-relay", "hp-failsafe-relay", version="000")
        )


def test_000_upgrades_to_001_unchanged() -> None:
    b = GwBoilerBackup000.model_validate(
        boiler("hp-failsafe-relay", "aquastat-ctrl-relay", version="000")
    ).upgrade()
    assert isinstance(b, GwBoilerBackup)
    assert b.failsafe_relay_name == "hp-failsafe-relay"
