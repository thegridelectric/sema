from typing import Literal
from pydantic import StrictInt
from sema.runtime.base import SemaType
from sema.runtime.enums import MarketPriceUnit
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import MarketSlotName
from sema.runtime.property_format import UUID4Str
from sema.runtime.types.latest_price import LatestPrice


class LatestPrice000(SemaType):
    """Sema: https://schemas.electricity.works/types/latest.price/000"""

    from_g_node_alias: LeftRightDot
    price_times1000: StrictInt
    price_unit: MarketPriceUnit
    market_slot_name: MarketSlotName
    message_id: UUID4Str
    type_name: Literal["latest.price"] = "latest.price"
    version: Literal["000"] = "000"

    def upgrade(self) -> LatestPrice:
        """
        - PriceTimes1000: renamed PriceX1000
        - Components: add, assigned as one Unknown component with the whole price
        - TariffAlias: add (optional)
        - CreatedMs: add (optional)
        """
        data = self.model_dump()
        data["price_x1000"] = data.pop("price_times1000")
        data["components"] = [
            {
                "name": "Unknown",
                "price_x1000": data["price_x1000"],
                "type_name": "price.component",
                "version": "000",
            }
        ]
        data["version"] = "001"
        return LatestPrice.model_validate(data)
