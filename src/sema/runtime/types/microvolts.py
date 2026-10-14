from typing import Literal
from pydantic import StrictInt, model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import SpaceheatName


class Microvolts(SemaType):
    """Sema: https://schemas.electricity.works/types/microvolts/100"""

    hw_uid: str
    about_node_name_list: list[SpaceheatName]
    micro_volts_list: list[StrictInt]
    type_name: Literal["microvolts"] = "microvolts"
    version: Literal["100"] = "100"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "Microvolts":
        """
        Axiom 1: ListLengthConsistency
        len(AboutNodeNameList) SHALL equal len(MicroVoltsList).
        """
        if len(self.about_node_name_list) != len(self.micro_volts_list):
            raise ValueError(
                "Axiom 1 failed: about_node_name_list and micro_volts_list must "
                f"have the same length (got {len(self.about_node_name_list)} and "
                f"{len(self.micro_volts_list)})."
            )
        return self
