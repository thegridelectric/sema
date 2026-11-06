from typing import Literal
from pydantic import StrictInt
from sema.runtime.base import SemaType
from sema.runtime.property_format import PositiveFloat
from sema.runtime.property_format import PositiveInt
from sema.runtime.types.heating_curve import HeatingCurve


class HeatingCurve000(SemaType):
    """Sema: https://schemas.electricity.works/types/heating.curve/000"""

    alpha_times10: StrictInt
    beta_times100: StrictInt
    gamma_ex6: StrictInt
    intermediate_power_kw: PositiveFloat
    intermediate_rswt_f: PositiveInt
    dd_power_kw: PositiveFloat
    dd_rswt_f: PositiveInt
    dd_delta_t_f: PositiveInt
    max_ewt_f: PositiveInt
    type_name: Literal["heating.curve"] = "heating.curve"
    version: Literal["000"] = "000"

    def upgrade(self) -> HeatingCurve:
        """
        - AlphaTimes10 -> BaselineAlphaTimes10
        - BetaTimes100 -> BaselineBetaTimes100
        - GammaEx6 -> BaselineGammaEx6
        - AlphaEx6: add
        - BetaEx6: add
        - GammaEx6: add
        - DeltaEx6: add
        - EpsilonEx6: add
        - ZetaEx6: add
        - EtaEx6: add
        - RhoTimes100: add
        - DdRoomTempF: add
        - MassFlowKgH: add
        """
        raise SemaType.upgrade_requires_context(
            "heating.curve:000 -> 001 needs the new load-forecast coefficients "
            "(AlphaEx6…RhoTimes100), DdRoomTempF, and MassFlowKgH that v000 does not carry; "
            "supply a v001 HeatingCurve from deployment or re-tune."
        )
