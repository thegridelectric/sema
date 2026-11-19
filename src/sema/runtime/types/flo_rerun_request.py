from typing import Literal, Self
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import NonNegativeInt
from sema.runtime.types.flo_params import FloParams
from sema.runtime.types.old_versions.flo_params_001 import FloParams001
from sema.runtime.types.old_versions.flo_params_002 import FloParams002
from sema.runtime.types.old_versions.flo_params_003 import FloParams003


class FloRerunRequest(SemaType):
    """Sema: https://schemas.electricity.works/types/flo.rerun.request/002"""

    params: FloParams001 | FloParams002 | FloParams003 | FloParams
    hp_forced_on_steps: list[NonNegativeInt]
    hp_forced_off_steps: list[NonNegativeInt]
    type_name: Literal["flo.rerun.request"] = "flo.rerun.request"
    version: Literal["002"] = "002"

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom 1: ForcedStepsWithinHorizon
        Each element of HpForcedOnSteps and HpForcedOffSteps SHALL be an integer in the
        half-open range from 0 up to but not including the length of
        Params.StepDurationMinutes.
        """
        horizon = len(self.params.step_duration_minutes)
        for name in ("hp_forced_on_steps", "hp_forced_off_steps"):
            out_of_range = [s for s in getattr(self, name) if not 0 <= s < horizon]
            if out_of_range:
                raise ValueError(
                    f"Axiom 1 (ForcedStepsWithinHorizon) failed: {name} must be in "
                    f"[0, {horizon}), got {out_of_range}."
                )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> Self:
        """
        Axiom 2: ForcedOnOffDisjoint
        No step index SHALL appear in both HpForcedOnSteps and HpForcedOffSteps.
        """
        both = sorted(set(self.hp_forced_on_steps) & set(self.hp_forced_off_steps))
        if both:
            raise ValueError(
                f"Axiom 2 (ForcedOnOffDisjoint) failed: steps cannot be forced both on "
                f"and off: {both}."
            )
        return self
