from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.flow_hall_params import FlowHallParams


class FlowHallParams101(SemaType):
    """Sema: https://schemas.electricity.works/types/flow.hall.params/101"""

    hw_uid: str
    actor_node_name: SpaceheatName
    flow_node_name: SpaceheatName
    publish_ticklist_period_s: PositiveInt
    publish_empty_ticklist_after_s: PositiveInt
    type_name: Literal["flow.hall.params"] = "flow.hall.params"
    version: Literal["101"] = "101"

    def upgrade(self) -> FlowHallParams:
        """
        - PicoBoardVariant: add
        - MicropythonVersion: add
        """
        raise SemaType.upgrade_requires_context(
            "FlowHallParams101 cannot be upgraded to "
            "FlowHallParams without context: v200 adds "
            "PicoBoardVariant and MicropythonVersion, which only the posting "
            "pico knows, and they SHALL NOT be fabricated."
        )
