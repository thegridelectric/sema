from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import GwHouseAlertKind
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.property_format import UUID4Str
from sema.runtime.types.channel_readings import ChannelReadings


class GwHouseAlertCleared(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.house.alert.cleared/000"""

    alert_id: UUID4Str
    src: LeftRightDot
    about_g_node_alias: LeftRightDot
    kind: GwHouseAlertKind
    cleared_ms: UTCMilliseconds
    evidence: list[ChannelReadings]
    type_name: Literal["gw.house.alert.cleared"] = "gw.house.alert.cleared"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwHouseAlertCleared":
        """
        Axiom 1: TerminalAssetAliasConstraint
        AboutGNodeAlias SHALL identify a TerminalAsset and therefore SHALL end with the suffix
        ".ta".
        """
        if not self.about_g_node_alias.endswith(".ta"):
            raise ValueError(
                f'TerminalAssetAliasConstraint: AboutGNodeAlias ({self.about_g_node_alias}) does not end with the suffix ".ta".'
            )
        return self
