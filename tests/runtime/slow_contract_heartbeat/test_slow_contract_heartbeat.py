"""slow.contract.heartbeat 003: the LTN amends the hour's contract with a
heartbeat whose Status is Amended, proved by mutation of the example."""

import pytest
from pydantic import ValidationError

from sema.runtime.base import UpgradeRequiresContext
from sema.runtime.codec import default_codec
from sema.runtime.enums.gw1_slow_dispatch_contract_status import (
    Gw1SlowDispatchContractStatus,
)
from sema.runtime.types.old_versions.slow_contract_heartbeat_002 import (
    SlowContractHeartbeat002,
)
from sema.runtime.types.slow_contract_heartbeat import SlowContractHeartbeat
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("slow.contract.heartbeat", "003")


def amended(p: dict) -> None:
    """The LTN's example heartbeat, as the amendment at the Final price."""
    p["PreviousStatus"] = "Confirmed"
    p["Status"] = "Amended"
    p["Contract"]["AvgPowerWatts"] = 4200
    p["Cause"] = "Final price 72.5 USD/MWh, offer raised"
    p["MessageCreatedMs"] = p["Contract"]["StartS"] * 1000 + 31_000


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("slow.contract.heartbeat", "003") == {
        1: [],
        2: ["a", "b", "c"],
        3: [],
        4: [],
        5: [],
        6: [],
    }


def test_example_round_trips() -> None:
    hb = SlowContractHeartbeat.model_validate(EXAMPLE)
    assert hb.contract.dispatch_terms == "dispatch.terms.first.isone.hack"
    assert SlowContractHeartbeat.model_validate(hb.model_dump(by_alias=True)) == hb


def test_the_ltn_amends_with_a_cause() -> None:
    hb = SlowContractHeartbeat.model_validate(mutated(EXAMPLE, amended))
    assert hb.status is Gw1SlowDispatchContractStatus.Amended
    assert hb.contract.avg_power_watts == 4200


def test_axiom_2a_refuses_an_amendment_from_the_scada() -> None:
    def mutate(p: dict) -> None:
        amended(p)
        p["FromNode"] = "s"
        p["WattHoursUsed"] = 120

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2, "a")


def test_axiom_3_refuses_an_amendment_without_a_cause() -> None:
    def mutate(p: dict) -> None:
        amended(p)
        del p["Cause"]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 3)


def test_a_002_reader_refuses_an_amendment() -> None:
    """On 002 the unknown status decodes to Unknown, which forbids the Cause an
    amendment carries (axiom 3): the scada reads 003 before the LTN amends."""

    def mutate(p: dict) -> None:
        amended(p)
        del p["Contract"]["DispatchTerms"]
        p["Contract"]["OilBoilerOn"] = False
        p["Contract"]["Version"] = "000"
        p["Version"] = "002"

    with pytest.raises(ValidationError, match="Axiom 3"):
        SlowContractHeartbeat002.model_validate(mutated(EXAMPLE, mutate))


def test_a_002_heartbeat_does_not_upgrade_without_context() -> None:
    old = SlowContractHeartbeat002.model_validate(
        example("slow.contract.heartbeat", "002")
    )
    with pytest.raises(UpgradeRequiresContext):
        old.upgrade()
