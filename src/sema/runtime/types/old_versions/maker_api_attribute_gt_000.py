from typing import Literal
from pydantic import StrictInt
from sema.runtime.base import SemaType
from sema.runtime.enums import SpaceheatTelemetryName
from sema.runtime.enums import SpaceheatUnit
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.maker_api_attribute_gt import MakerApiAttributeGt


class MakerApiAttributeGt000(SemaType):
    """Sema: https://schemas.electricity.works/types/maker.api.attribute.gt/000"""

    attribute_name: str
    channel_name: SpaceheatName
    node_name: SpaceheatName
    telemetry_name: SpaceheatTelemetryName
    unit: SpaceheatUnit
    exponent: StrictInt
    interpret_as_number: bool
    enabled: bool
    web_poll_enabled: bool
    web_listen_enabled: bool
    report_missing: bool
    report_parse_error: bool
    type_name: Literal["maker.api.attribute.gt"] = "maker.api.attribute.gt"
    version: Literal["000"] = "000"

    def upgrade(self) -> "MakerApiAttributeGt":
        """
        Enabled dropped: whether a channel is read is the layout's DisabledChannelNames, not a per-attribute flag. WebPollEnabled and WebListenEnabled stay (they name the transport path).
        """
        data = self.model_dump()
        data.pop("enabled", None)
        data["version"] = "001"
        return MakerApiAttributeGt.model_validate(data)
