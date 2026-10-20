from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.types.old_versions.layout_lite_011 import LayoutLite011
from sema.runtime.types.old_versions.layout_lite_012 import LayoutLite012


class LayoutBundle(SemaType):
    """Sema: https://schemas.electricity.works/types/layout.bundle/000"""

    layouts: list[LayoutLite011 | LayoutLite012]
    send_time_ms: UTCMilliseconds
    proof: str | None = None
    type_name: Literal["layout.bundle"] = "layout.bundle"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "LayoutBundle":
        """
        Axiom 1: OneLayoutPerSender
        No two entries in Layouts SHALL have the same FromGNodeAlias.
        """
        senders = [layout.from_g_node_alias for layout in self.layouts]
        if len(senders) != len(set(senders)):
            raise ValueError(
                "Axiom 1 failed: each FromGNodeAlias may appear once in layouts."
            )
        return self
