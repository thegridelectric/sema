from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.enums import PicoBoardVariant
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.flow_hall_params import FlowHallParams


class FlowHallParams200(SemaType):
    """Sema: https://schemas.electricity.works/types/flow.hall.params/200"""

    hw_uid: str
    actor_node_name: SpaceheatName
    flow_node_name: SpaceheatName
    publish_ticklist_period_s: PositiveInt
    publish_empty_ticklist_after_s: PositiveInt
    pico_board_variant: PicoBoardVariant
    micropython_version: str
    type_name: Literal["flow.hall.params"] = "flow.hall.params"
    version: Literal["200"] = "200"

    def upgrade(self) -> FlowHallParams:
        """
        - FirmwareCommit: add
        """
        raise SemaType.upgrade_requires_context(
            "FlowHallParams200 cannot be upgraded to "
            "FlowHallParams without context: v210 adds "
            "FirmwareCommit, which only the posting pico knows, and it SHALL "
            "NOT be fabricated."
        )
