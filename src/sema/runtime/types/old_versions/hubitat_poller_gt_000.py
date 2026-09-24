from typing import Literal
from pydantic import StrictFloat
from sema.runtime.base import SemaType
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import UUID4Str
from sema.runtime.types.hubitat_poller_gt import HubitatPollerGt
from sema.runtime.types.old_versions.maker_api_attribute_gt_000 import (
    MakerApiAttributeGt000,
)


class HubitatPollerGt000(SemaType):
    """Sema: https://schemas.electricity.works/types/hubitat.poller.gt/000"""

    hubitat_component_id: UUID4Str
    device_id: PositiveInt
    attributes: list[MakerApiAttributeGt000]
    enabled: bool
    web_listen_enabled: bool
    poll_period_seconds: StrictFloat
    type_name: Literal["hubitat.poller.gt"] = "hubitat.poller.gt"
    version: Literal["000"] = "000"

    def upgrade(self) -> "HubitatPollerGt":
        """
        Enabled dropped: whether a device is polled is the layout's DisabledNodeNames, not a per-poller flag; Attributes are maker.api.attribute.gt:001. WebListenEnabled stays (it names the transport path).
        """
        data = self.model_dump()
        data.pop("enabled", None)
        data["attributes"] = [a.upgrade().model_dump() for a in self.attributes]
        data["version"] = "001"
        return HubitatPollerGt.model_validate(data)
