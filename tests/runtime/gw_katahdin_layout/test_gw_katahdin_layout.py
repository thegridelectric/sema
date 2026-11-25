"""Rejecting tests for gw.katahdin.layout/000's boiler backup axioms.

The vanilla fixture is a generated Katahdin layout with a boiler backup that
the word accepts. Each test mutates a copy of it so that exactly one axiom
fires, and asserts the word refuses it.
"""

import json
from pathlib import Path
from typing import Any, Callable

import pytest

from sema.runtime.types.gw_katahdin_layout import GwKatahdinLayout

FIXTURE = Path(__file__).parent / "fixtures" / "vanilla.json"


@pytest.fixture(scope="module")
def vanilla() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text())


def reject(
    vanilla: dict[str, Any], mutate: Callable[[dict[str, Any]], None], axiom: str
) -> None:
    d = json.loads(json.dumps(vanilla))
    mutate(d)
    with pytest.raises(ValueError, match=axiom):
        GwKatahdinLayout.model_validate(d)


def intercept_config(d: dict[str, Any]) -> dict[str, Any]:
    name = d["Hydronic"]["Backup"]["InterceptRelayName"]
    return next(
        cfg
        for c in d["Components"]
        for cfg in c.get("ConfigList", [])
        if cfg.get("TypeName") == "relay.control.config" and cfg["ActorName"] == name
    )


def test_vanilla_validates(vanilla: dict[str, Any]) -> None:
    layout = GwKatahdinLayout.model_validate(vanilla)
    assert layout.hydronic.backup is not None


def test_axiom_32_b_intercept_relay_is_not_a_relay(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["Backup"]["InterceptRelayName"] = "backup"

    reject(vanilla, mutate, "Axiom 32")


def test_axiom_35_intercept_relay_holds_the_boiler_off_at_rest(
    vanilla: dict[str, Any],
) -> None:
    def mutate(d: dict[str, Any]) -> None:
        cfg = intercept_config(d)
        cfg["DeEnergizedState"], cfg["EnergizedState"] = "Scada", "Boiler"
        cfg["DeEnergizingEvent"], cfg["EnergizingEvent"] = (
            "SwitchToScada",
            "SwitchToBoiler",
        )

    reject(vanilla, mutate, "Axiom 35")
