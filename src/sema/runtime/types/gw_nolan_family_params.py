from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1SeasonalStorageMode


class GwNolanFamilyParams(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.nolan.family.params/000"""

    keep_buffer_full: bool
    seasonal_storage_mode: Gw1SeasonalStorageMode
    type_name: Literal["gw.nolan.family.params"] = "gw.nolan.family.params"
    version: Literal["000"] = "000"
