from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.enums import PicoBoardVariant
from sema.runtime.property_format import FirmwareCommit
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName


class FlowHallParams(SemaType):
    """Sema: https://schemas.electricity.works/types/flow.hall.params/210"""

    hw_uid: str
    actor_node_name: SpaceheatName
    flow_node_name: SpaceheatName
    publish_ticklist_period_s: PositiveInt
    publish_empty_ticklist_after_s: PositiveInt
    pico_board_variant: PicoBoardVariant
    micropython_version: str
    firmware_commit: FirmwareCommit
    type_name: Literal["flow.hall.params"] = "flow.hall.params"
    version: Literal["210"] = "210"
