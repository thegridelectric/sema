from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1Quantity
from sema.runtime.enums import Gw1Unit
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import NonEmptyString
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName
from sema.runtime.property_format import UUID4Str
from sema.runtime.property_format import UtcIso8601Seconds
from sema.runtime.types.gw1_unit_quantity_projection import Gw1UnitQuantityProjection


class GwServiceChannelGt(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.service.channel.gt/000"""

    name: SpaceheatName
    display_name: NonEmptyString
    quantity: Gw1Quantity
    unit: Gw1Unit
    declaring_service_alias: LeftRightDot
    terminal_asset_alias: LeftRightDot | None = None
    input_channel_names: list[SpaceheatName]
    strategy: SpaceheatName
    window_s: PositiveInt | None = None
    start: UtcIso8601Seconds
    id: UUID4Str
    type_name: Literal["gw.service.channel.gt"] = "gw.service.channel.gt"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwServiceChannelGt":
        """
        Axiom 1: UnitQuantityConsistency
        Quantity SHALL equal the Quantity defined by the canonical
        gw1.unit.quantity.projection:001 instance for the specified Unit.
        """
        expected = Gw1UnitQuantityProjection.project(Gw1Unit(self.unit.value))
        if self.quantity != expected:
            raise ValueError(
                "Axiom 1 failed: quantity must match the canonical quantity for unit."
            )
        return self
