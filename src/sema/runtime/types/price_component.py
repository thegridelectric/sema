from typing import Literal
from pydantic import StrictInt
from sema.runtime.base import SemaType
from sema.runtime.enums import PriceComponentName


class PriceComponent(SemaType):
    """Sema: https://schemas.electricity.works/types/price.component/000"""

    name: PriceComponentName
    price_x1000: StrictInt
    type_name: Literal["price.component"] = "price.component"
    version: Literal["000"] = "000"
