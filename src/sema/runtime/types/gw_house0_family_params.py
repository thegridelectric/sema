from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1SeasonalStorageMode


class GwHouse0FamilyParams(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.house0.family.params/000"""

    use_sieg_loop: bool
    keep_buffer_full: bool
    seasonal_storage_mode: Gw1SeasonalStorageMode
    type_name: Literal["gw.house0.family.params"] = "gw.house0.family.params"
    version: Literal["000"] = "000"
