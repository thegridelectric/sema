from typing import Literal
from pydantic import StrictInt, model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import SpaceheatTelemetryName
from sema.runtime.property_format import SpaceheatName


class MultichannelSnapshot(SemaType):
    """Sema: https://schemas.electricity.works/types/multichannel.snapshot/000"""

    hw_uid: str
    channel_name_list: list[SpaceheatName]
    measurement_list: list[StrictInt]
    unit_list: list[SpaceheatTelemetryName]
    type_name: Literal["multichannel.snapshot"] = "multichannel.snapshot"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "MultichannelSnapshot":
        """
        Axiom 1: ListLengthConsistency
        len(ChannelNameList), len(MeasurementList) and len(UnitList) SHALL be equal.
        """
        lengths = (
            len(self.channel_name_list),
            len(self.measurement_list),
            len(self.unit_list),
        )
        if len(set(lengths)) != 1:
            raise ValueError(
                "Axiom 1 failed: channel_name_list, measurement_list and unit_list "
                f"must have the same length (got {lengths})."
            )
        return self
