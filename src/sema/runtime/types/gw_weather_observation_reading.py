from typing import Literal
from pydantic import StrictInt
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1Quantity
from sema.runtime.property_format import LeftRightDot


class GwWeatherObservationReading(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.weather.observation.reading/000"""

    channel_name: LeftRightDot
    quantity: Gw1Quantity
    value: StrictInt
    type_name: Literal["gw.weather.observation.reading"] = (
        "gw.weather.observation.reading"
    )
    version: Literal["000"] = "000"
