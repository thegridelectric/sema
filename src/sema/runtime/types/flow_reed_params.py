from typing import Literal
from pydantic import StrictInt
from sema.runtime.base import SemaType
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName


class FlowReedParams(SemaType):
    """Sema: https://schemas.electricity.works/types/flow.reed.params/101"""

    hw_uid: str
    actor_node_name: SpaceheatName
    flow_node_name: SpaceheatName
    publish_ticklist_length: PositiveInt
    publish_any_ticklist_after_s: PositiveInt
    deadband_milliseconds: StrictInt
    type_name: Literal["flow.reed.params"] = "flow.reed.params"
    version: Literal["101"] = "101"
