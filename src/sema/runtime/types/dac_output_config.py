from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.enums import I2cDacChannel
from sema.runtime.property_format import SpaceheatName


class DacOutputConfig(SemaType):
    """Sema: https://schemas.electricity.works/types/dac.output.config/000"""

    channel_name: SpaceheatName
    actor_name: SpaceheatName
    dac_channel: I2cDacChannel
    type_name: Literal["dac.output.config"] = "dac.output.config"
    version: Literal["000"] = "000"
