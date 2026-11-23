from typing import Literal
from pydantic import StrictFloat
from sema.runtime.base import SemaType


class CopCurve(SemaType):
    """Sema: https://schemas.electricity.works/types/cop.curve/000"""

    intercept: StrictFloat
    lwt_minus_oat_coeff: StrictFloat
    type_name: Literal["cop.curve"] = "cop.curve"
    version: Literal["000"] = "000"
