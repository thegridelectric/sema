from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1SeasonalStorageMode
from sema.runtime.enums import Gw1ServiceMode
from sema.runtime.enums import GwDispatchRefusalReason
from sema.runtime.enums import GwStandbyPosture
from sema.runtime.enums import GwTopState
from sema.runtime.enums import TaValidationState
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCMilliseconds


class GwHouseOperatingStatus(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.house.operating.status/000"""

    scada_alias: LeftRightDot
    validation_state: TaValidationState
    standby: bool
    standby_posture: GwStandbyPosture
    seasonal_storage_mode: Gw1SeasonalStorageMode
    service_mode: Gw1ServiceMode
    accepts_dispatch: bool
    dispatch_refusal_reason: GwDispatchRefusalReason | None = None
    top_state: GwTopState
    ltn_dispatching: bool
    unix_ms: UTCMilliseconds
    type_name: Literal["gw.house.operating.status"] = "gw.house.operating.status"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwHouseOperatingStatus":
        """
        Axiom 1: RefusalReasonPresence
        DispatchRefusalReason SHALL be present if and only if AcceptsDispatch is false.
        """
        if self.accepts_dispatch and self.dispatch_refusal_reason is not None:
            raise ValueError(
                "Axiom 1 (RefusalReasonPresence) failed: AcceptsDispatch true "
                "forbids DispatchRefusalReason."
            )
        if not self.accepts_dispatch and self.dispatch_refusal_reason is None:
            raise ValueError(
                "Axiom 1 (RefusalReasonPresence) failed: AcceptsDispatch false "
                "requires DispatchRefusalReason."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "GwHouseOperatingStatus":
        """
        Axiom 2: StandbyRefusesDispatch
        If Standby is true, AcceptsDispatch SHALL be false and DispatchRefusalReason SHALL
        be Standby.
        """
        if self.standby and (
            self.accepts_dispatch
            or self.dispatch_refusal_reason is not GwDispatchRefusalReason.Standby
        ):
            raise ValueError(
                "Axiom 2 (StandbyRefusesDispatch) failed: Standby requires "
                "AcceptsDispatch false with DispatchRefusalReason Standby."
            )
        return self
