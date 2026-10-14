from typing import Literal
from pydantic import StrictFloat, StrictInt
from sema.runtime.base import SemaType
from sema.runtime.types.ha1_params import Ha1Params


class Ha1Params005(SemaType):
    """Sema: https://schemas.electricity.works/types/ha1.params/005"""

    alpha_times10: StrictInt
    beta_times100: StrictInt
    gamma_ex6: StrictInt
    intermediate_power_kw: StrictFloat
    intermediate_rswt_f: StrictInt
    dd_power_kw: StrictFloat
    dd_rswt_f: StrictInt
    dd_delta_t_f: StrictInt
    hp_max_kw_th: StrictFloat
    max_ewt_f: StrictInt
    load_overestimation_percent: StrictInt
    cop_intercept: StrictFloat | None = None
    cop_oat_coeff: StrictFloat | None = None
    cop_lwt_coeff: StrictFloat | None = None
    cop_min: StrictFloat | None = None
    cop_min_oat_f: StrictFloat | None = None
    type_name: Literal["ha1.params"] = "ha1.params"
    version: Literal["005"] = "005"

    def upgrade(self) -> Ha1Params:
        """
        HpMaxKwEl replaces HpMaxKwTh, required; the five Cop fields
        required; HpTurnOnMinutes added, required (the shape every scada
        has published at this version)
        """
        raise SemaType.upgrade_requires_context(
            "Ha1Params005 cannot be upgraded to "
            "Ha1Params without context: v006 requires "
            "HpMaxKwEl, which the heat pump's thermal maximum does not give, "
            "and the five Cop fields v005 leaves optional; only the house's "
            "operational params know them, and they SHALL NOT be fabricated."
        )
