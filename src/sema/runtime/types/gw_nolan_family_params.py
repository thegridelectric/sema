from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1SeasonalStorageMode
from sema.runtime.property_format import PositiveInt


class GwNolanFamilyParams(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.nolan.family.params/000"""

    keep_buffer_full: bool
    seasonal_storage_mode: Gw1SeasonalStorageMode
    buffer_full_f: PositiveInt
    buffer_charge_f: PositiveInt
    type_name: Literal["gw.nolan.family.params"] = "gw.nolan.family.params"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwNolanFamilyParams":
        """
        Axiom 1: ChargeBelowFull
        BufferChargeF SHALL be less than BufferFullF.
        """
        if self.buffer_charge_f >= self.buffer_full_f:
            raise ValueError(
                "Axiom 1 (ChargeBelowFull) failed: BufferChargeF "
                f"{self.buffer_charge_f} is not below BufferFullF {self.buffer_full_f}"
            )
        return self
