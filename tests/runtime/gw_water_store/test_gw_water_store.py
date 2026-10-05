"""gw.water.store 000: the tank count and its bound."""

import pytest
from pydantic import ValidationError

from sema.runtime.types.gw_water_store import GwWaterStore


def store(tanks: object) -> dict[str, object]:
    return {"TotalStoreTanks": tanks, "TypeName": "gw.water.store", "Version": "000"}


@pytest.mark.parametrize("tanks", [1, 6])
def test_one_to_six_tanks_validate(tanks: int) -> None:
    assert GwWaterStore.model_validate(store(tanks)).total_store_tanks == tanks


def test_no_tanks_is_not_a_water_store() -> None:
    with pytest.raises(ValidationError):
        GwWaterStore.model_validate(store(0))


def test_axiom_1_more_than_six_tanks() -> None:
    with pytest.raises(ValidationError, match="(?i)axiom 1"):
        GwWaterStore.model_validate(store(7))
