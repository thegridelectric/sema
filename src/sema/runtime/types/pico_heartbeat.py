from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.enums import PicoResetCause
from sema.runtime.property_format import NonNegativeInt


class PicoHeartbeat(SemaType):
    """Sema: https://schemas.electricity.works/types/pico.heartbeat/000"""

    hw_uid: str
    uptime_s: NonNegativeInt
    reset_cause: PicoResetCause
    type_name: Literal["pico.heartbeat"] = "pico.heartbeat"
    version: Literal["000"] = "000"
