from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import IanaTimezoneStr
from sema.runtime.property_format import LeftRightDot
from sema.runtime.types.gw_tou_window import GwTouWindow


class GwTouTariff(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.tou.tariff/000"""

    alias: LeftRightDot
    display_name: str
    timezone_str: IanaTimezoneStr
    on_peak_windows: list[GwTouWindow]
    type_name: Literal["gw.tou.tariff"] = "gw.tou.tariff"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwTouTariff":
        """
        Axiom 1: PerDayWindowNonOverlap
        For each day of the week, the windows in OnPeakWindows whose Days include that day
        SHALL NOT overlap one another.
        """
        days = {day for w in self.on_peak_windows for day in w.days}
        for day in days:
            todays = sorted(
                (w for w in self.on_peak_windows if day in w.days),
                key=lambda w: w.start,
            )
            for earlier, later in zip(todays, todays[1:]):
                if later.start < earlier.end:
                    raise ValueError(
                        "Axiom 1 (PerDayWindowNonOverlap) failed: on "
                        f"{day} window {later.start}-{later.end} overlaps "
                        f"{earlier.start}-{earlier.end}."
                    )
        return self
