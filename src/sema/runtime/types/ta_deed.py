from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import TaValidationState
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCSeconds
from sema.runtime.property_format import UUID4Str


class TaDeed(SemaType):
    """Sema: https://schemas.electricity.works/types/ta.deed/001"""

    ta_id: UUID4Str
    ta_alias: LeftRightDot
    validation_state: TaValidationState
    validator_alias: LeftRightDot
    issued_s: UTCSeconds
    type_name: Literal["ta.deed"] = "ta.deed"
    version: Literal["001"] = "001"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "TaDeed":
        """
        Axiom 1: SimulatedAssetNeverWorld
        If ValidationState is ValidatedSimulatedAsset, the first segment of TaAlias SHALL
        NOT be "w": a simulated asset holds no deed in the world universe.
        """
        if (
            self.validation_state == "ValidatedSimulatedAsset"
            and self.ta_alias.split(".")[0] == "w"
        ):
            raise ValueError(
                "Axiom 1 (SimulatedAssetNeverWorld) failed: a ValidatedSimulatedAsset "
                f"deed cannot carry a world-universe alias, got TaAlias {self.ta_alias}."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "TaDeed":
        """
        Axiom 2: NoRealAssetInDUniverse
        If the first segment of TaAlias begins with "d", ValidationState SHALL be
        UnValidated or ValidatedSimulatedAsset: a d universe is all simulated and
        holds no real asset.
        """
        if self.ta_alias.split(".")[0].startswith(
            "d"
        ) and self.validation_state not in (
            "UnValidated",
            "ValidatedSimulatedAsset",
        ):
            raise ValueError(
                "Axiom 2 (NoRealAssetInDUniverse) failed: a d universe holds no real "
                f"asset, got ValidationState {self.validation_state} on TaAlias "
                f"{self.ta_alias}."
            )
        return self
