from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import SemaVersion
from sema.runtime.property_format import SpaceheatName


class GwStateMachine(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.state.machine/000"""

    node_name: SpaceheatName
    state_enum: LeftRightDot
    state_enum_version: SemaVersion
    type_name: Literal["gw.state.machine"] = "gw.state.machine"
    version: Literal["000"] = "000"
