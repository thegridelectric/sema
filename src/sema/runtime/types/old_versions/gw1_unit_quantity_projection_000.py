from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums.old_versions.gw1_quantity_001 import Gw1Quantity001
from sema.runtime.enums.old_versions.gw1_unit_001 import Gw1Unit001
from sema.runtime.types.gw1_unit_quantity_projection import Gw1UnitQuantityProjection


_PROJECTION = {
    Gw1Unit001.Unknown: Gw1Quantity001.Unknown,
    Gw1Unit001.Unitless: Gw1Quantity001.Unitless,
    Gw1Unit001.FahrenheitX100: Gw1Quantity001.Temperature,
    Gw1Unit001.Watts: Gw1Quantity001.Power,
    Gw1Unit001.WattHours: Gw1Quantity001.Energy,
    Gw1Unit001.Gallons: Gw1Quantity001.Volume,
    Gw1Unit001.GpmX100: Gw1Quantity001.FlowRate,
    Gw1Unit001.Seconds: Gw1Quantity001.Time,
    Gw1Unit001.SecondsX10: Gw1Quantity001.Time,
    Gw1Unit001.Milliseconds: Gw1Quantity001.Time,
}


class Gw1UnitQuantityProjection000(SemaType):
    """Sema: https://schemas.electricity.works/types/gw1.unit.quantity.projection/000"""

    unit: Gw1Unit001
    quantity: Gw1Quantity001
    type_name: Literal["gw1.unit.quantity.projection"] = "gw1.unit.quantity.projection"
    version: Literal["000"] = "000"

    @classmethod
    def project(cls, unit: Gw1Unit001) -> Gw1Quantity001:
        expected = _PROJECTION.get(unit)
        if expected is None:
            raise ValueError(f"No projection defined for unit {unit!r}.")
        return expected

    @model_validator(mode="after")
    def check_axiom_1(self) -> "Gw1UnitQuantityProjection000":
        """
        Axiom 1: EnumeratedProjectionMapping
        Every (Unit, Quantity) pair SHALL match the mapping declared in
        x-gridworks.projection.table. Any combination not present in the table is invalid.
        """
        expected = self.project(self.unit)
        if expected != self.quantity:
            raise ValueError(
                "Axiom 1 failed: unit and quantity do not match the enumerated projection."
            )
        return self

    def upgrade(self) -> Gw1UnitQuantityProjection:
        """
        - Unit: gw1.unit 001 -> 003
        - Quantity: gw1.quantity 001 -> 003
        - projection.table: add DollarsX1000 -> Currency, MilesPerHourX1000 -> WindSpeed, KilowattHoursX1000 -> Energy, WattsPerSquareMeter -> Irradiance
        """
        data = self.model_dump()
        data["unit"] = self.unit.value
        data["quantity"] = self.quantity.value
        data["version"] = "001"
        return Gw1UnitQuantityProjection.model_validate(data)
