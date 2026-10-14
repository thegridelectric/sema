from typing import Literal
from sema.runtime.base import SemaType


class NewPico(SemaType):
    """Sema: https://schemas.electricity.works/types/new.pico/100"""

    hw_uid: str
    type_name: Literal["new.pico"] = "new.pico"
    version: Literal["100"] = "100"
