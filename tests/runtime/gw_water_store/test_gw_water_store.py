"""gw.water.store 000: the tank count and its bound, gallons and sensors per tank."""

import pytest
from pydantic import ValidationError

from sema.runtime.types.gw_water_store import GwWaterStore


def store(
    tanks: object, gallons: object = 120, sensors: object = 3
) -> dict[str, object]:
    return {
        "TotalStoreTanks": tanks,
        "GallonsPerTank": gallons,
        "TempSensorsPerTank": sensors,
        "TypeName": "gw.water.store",
        "Version": "000",
    }


@pytest.mark.parametrize("tanks", [1, 6])
def test_one_to_six_tanks_validate(tanks: int) -> None:
    assert GwWaterStore.model_validate(store(tanks)).total_store_tanks == tanks


def test_no_tanks_is_not_a_water_store() -> None:
    with pytest.raises(ValidationError):
        GwWaterStore.model_validate(store(0))


def test_axiom_1_more_than_six_tanks() -> None:
    with pytest.raises(ValidationError, match="(?i)axiom 1"):
        GwWaterStore.model_validate(store(7))


@pytest.mark.parametrize("field", ["GallonsPerTank", "TempSensorsPerTank"])
def test_zero_per_tank_is_refused(field: str) -> None:
    with pytest.raises(ValidationError):
        GwWaterStore.model_validate({**store(3), field: 0})


def test_gallons_and_sensors_are_required() -> None:
    d = store(3)
    del d["GallonsPerTank"]
    with pytest.raises(ValidationError):
        GwWaterStore.model_validate(d)
