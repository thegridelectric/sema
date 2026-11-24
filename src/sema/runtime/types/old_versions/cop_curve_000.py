from typing import Literal
from pydantic import StrictFloat
from sema.runtime.base import SemaType
from sema.runtime.types.cop_curve import CopCurve


class CopCurve000(SemaType):
    """Sema: https://schemas.electricity.works/types/cop.curve/000"""

    intercept: StrictFloat
    oat_coeff: StrictFloat
    lwt_coeff: StrictFloat
    min: StrictFloat
    min_oat_f: StrictFloat
    type_name: Literal["cop.curve"] = "cop.curve"
    version: Literal["000"] = "000"

    def upgrade(self) -> CopCurve:
        """
        - Lift-based model: Intercept + LwtMinusOatCoeff * max(0, LwtF - OatF);
          OatCoeff, LwtCoeff, Min, MinOatF dropped. A 000 is a different fit
          and does not upgrade.
        """
        raise SemaType.upgrade_requires_context(
            "CopCurve000 cannot be upgraded to "
            "CopCurve: v001 is a regression against the "
            "lift from outdoor air to leaving water, and its coefficients are "
            "not derivable from the v000 outdoor-air model; they SHALL NOT be "
            "fabricated."
        )
