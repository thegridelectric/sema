from typing import Literal
from sema.runtime.base import SemaType


class FloTuningAlice(SemaType):
    """Sema: https://schemas.electricity.works/types/flo.tuning.alice/000"""

    type_name: Literal["flo.tuning.alice"] = "flo.tuning.alice"
    version: Literal["000"] = "000"
