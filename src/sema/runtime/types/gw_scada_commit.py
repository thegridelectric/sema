from typing import Literal
from sema.runtime.base import SemaType
from sema.runtime.property_format import GitCommit
from sema.runtime.property_format import LeftRightDot
from sema.runtime.property_format import UTCMilliseconds


class GwScadaCommit(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.scada.commit/000"""

    scada_alias: LeftRightDot
    git_commit: GitCommit
    message_created_ms: UTCMilliseconds
    type_name: Literal["gw.scada.commit"] = "gw.scada.commit"
    version: Literal["000"] = "000"
