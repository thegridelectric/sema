from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import NonEmptyString
from sema.runtime.property_format import UUID4Str


class GwOpsgenieAlertClose(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.opsgenie.alert.close/000"""

    alias: UUID4Str
    source: LeftRightDot
    note: NonEmptyString
    type_name: Literal["gw.opsgenie.alert.close"] = "gw.opsgenie.alert.close"
    version: Literal["000"] = "000"
