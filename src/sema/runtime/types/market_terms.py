from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import GwMarketProductName
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCMilliseconds
from sema.runtime.property_format import UTCSeconds


class MarketTerms(SemaType):
    """Sema: https://schemas.electricity.works/types/market.terms/000"""

    market_maker_alias: LeftRightDot
    market_product_name: GwMarketProductName
    dispatch_terms: LeftRightDot
    effective_s: UTCSeconds
    created_ms: UTCMilliseconds
    type_name: Literal["market.terms"] = "market.terms"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "MarketTerms":
        """
        Axiom 1: EffectiveOnSlotBoundary
        EffectiveS SHALL be a multiple of the slot length, in seconds, that
        MarketProductName encodes, so no slot runs under two terms.
        """
        import re  # local: the generator renders no module-level imports for axiom bodies

        token = self.market_product_name.value
        match = re.match(r"^(?:rt|da)(\d+)", token)
        if match is None:
            raise ValueError(
                "Axiom 1 (EffectiveOnSlotBoundary) failed: MarketProductName "
                f"{token} encodes no slot length."
            )
        slot_s = int(match.group(1)) * 60
        if self.effective_s % slot_s != 0:
            raise ValueError(
                "Axiom 1 (EffectiveOnSlotBoundary) failed: EffectiveS must be a "
                f"multiple of {slot_s} for {token}, got {self.effective_s}."
            )
        return self
