"""slow.dispatch.contract 001: the contract names the dispatch terms it is an
instance of, proved by mutation of the example."""

import pytest
from pydantic import ValidationError

from sema.runtime.base import UpgradeRequiresContext
from sema.runtime.types.old_versions.slow_dispatch_contract_000 import (
    SlowDispatchContract000,
)
from sema.runtime.types.slow_dispatch_contract import SlowDispatchContract
from tests.runtime.refusal import axioms, example, mutated

EXAMPLE = example("slow.dispatch.contract", "001")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("slow.dispatch.contract", "001") == {1: []}


def test_example_round_trips() -> None:
    contract = SlowDispatchContract.model_validate(EXAMPLE)
    assert contract.dispatch_terms == "dispatch.terms.first.isone.hack"
    assert (
        SlowDispatchContract.model_validate(contract.model_dump(by_alias=True))
        == contract
    )


def test_a_contract_without_dispatch_terms_is_refused() -> None:
    def mutate(p: dict) -> None:
        del p["DispatchTerms"]

    with pytest.raises(ValidationError):
        SlowDispatchContract.model_validate(mutated(EXAMPLE, mutate))


def test_a_000_contract_does_not_upgrade_without_context() -> None:
    old = SlowDispatchContract000.model_validate(
        example("slow.dispatch.contract", "000")
    )
    with pytest.raises(UpgradeRequiresContext):
        old.upgrade()
