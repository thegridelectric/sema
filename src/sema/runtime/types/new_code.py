from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.property_format import SpaceheatName


class NewCode(SemaType):
    """Sema: https://schemas.electricity.works/types/new.code/100"""

    hw_uid: str
    actor_node_name: SpaceheatName
    type_name: Literal["new.code"] = "new.code"
    version: Literal["100"] = "100"
