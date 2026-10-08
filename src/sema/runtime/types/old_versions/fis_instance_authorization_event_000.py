from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import FisAuthorizationDecision
from sema.runtime.enums import FisAuthorizationReason
from sema.runtime.enums import GNodeInstanceTransport
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import NonEmptyString
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.property_format import UUID4Str
from sema.runtime.property_format import UniverseRun
from sema.runtime.types.fis_instance_authorization_event import (
    FisInstanceAuthorizationEvent,
)


_PROJECTION = {
    FisAuthorizationReason.MalformedRequest: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.PrincipalNotFound: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.PrincipalSuspended: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.RunOutsideUniverse: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.NotInRegistry: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.AliasMismatch: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.ClassMismatch: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.InstanceRevoked: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.KillUnconfirmed: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.LeaseRace: FisAuthorizationDecision.Denied,
    FisAuthorizationReason.IdempotentReconnect: FisAuthorizationDecision.Authorized,
    FisAuthorizationReason.Superseded: FisAuthorizationDecision.Authorized,
}


class FisInstanceAuthorizationEvent000(SemaType):
    """Sema: https://schemas.electricity.works/types/fis.instance.authorization.event/000"""

    event_id: UUID4Str
    principal_id: UUID4Str
    instance_id: UUID4Str
    run: UniverseRun
    alias: LeftRightDot | None = None
    g_node_class: NonEmptyString | None = None
    transport: GNodeInstanceTransport
    decision: FisAuthorizationDecision
    reason: FisAuthorizationReason
    decided_at_unix_ms: UTCMilliseconds
    type_name: Literal["fis.instance.authorization.event"] = (
        "fis.instance.authorization.event"
    )
    version: Literal["000"] = "000"

    @classmethod
    def project(cls, reason: FisAuthorizationReason) -> FisAuthorizationDecision:
        expected = _PROJECTION.get(reason)
        if expected is None:
            raise ValueError(f"No projection defined for reason {reason!r}.")
        return expected

    @model_validator(mode="after")
    def check_axiom_1(self) -> "FisInstanceAuthorizationEvent000":
        """
        Axiom 1: ReasonDeterminesDecision
        Decision SHALL equal the value the projection table maps Reason to.
        """
        expected = self.project(self.reason)
        if self.decision != expected:
            raise ValueError(
                f"Axiom 1 failed: Reason {self.reason.value} maps to Decision "
                f"{expected.value}, not {self.decision.value}."
            )
        return self

    def upgrade(self) -> FisInstanceAuthorizationEvent:
        """
        InstanceId and Run optional, so a verdict on a request whose claims did
        not decode is recorded; PrincipalId and Transport stay required
        """
        data = self.model_dump()
        data["version"] = "001"
        return FisInstanceAuthorizationEvent.model_validate(data)
