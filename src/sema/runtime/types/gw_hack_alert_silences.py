from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import LeftRightDot


class GwHackAlertSilences(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.hack.alert.silences/000"""

    src: LeftRightDot
    silenced_g_node_aliases: list[LeftRightDot]
    type_name: Literal["gw.hack.alert.silences"] = "gw.hack.alert.silences"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwHackAlertSilences":
        """
        Axiom 1: TerminalAssetAliases
        Every value of SilencedGNodeAliases SHALL identify a TerminalAsset and therefore
        SHALL end with the suffix ".ta".
        """
        for alias in self.silenced_g_node_aliases:
            if not alias.endswith(".ta"):
                raise ValueError(
                    f'TerminalAssetAliases: Axiom 1: SilencedGNodeAliases entry ({alias}) does not end with the suffix ".ta".'
                )
        return self
