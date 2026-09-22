from typing import Literal
from pydantic import StrictFloat, model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import PicoBoardVariant
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.tank_module_params import TankModuleParams


class TankModuleParams200(SemaType):
    """Sema: https://schemas.electricity.works/types/tank.module.params/200"""

    hw_uid: str
    actor_node_name: SpaceheatName
    pico_a_b: str | None = None
    capture_period_s: PositiveInt
    samples: PositiveInt
    num_sample_averages: PositiveInt
    async_capture_delta_micro_volts: PositiveInt
    capture_offset_s: StrictFloat | None = None
    pico_board_variant: PicoBoardVariant
    micropython_version: str
    type_name: Literal["tank.module.params"] = "tank.module.params"
    version: Literal["200"] = "200"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "TankModuleParams200":
        """
        Axiom 1: PicoABIsAOrB
        If PicoAB is present it SHALL be "a" or "b".
        """
        if self.pico_a_b is not None and self.pico_a_b not in ("a", "b"):
            raise ValueError(
                f"Axiom 1: If PicoAB is present it SHALL be a or b, not {self.pico_a_b!r}"
            )
        return self

    def upgrade(self) -> TankModuleParams:
        """
        - FirmwareCommit: add
        """
        raise SemaType.upgrade_requires_context(
            "TankModuleParams200 cannot be upgraded to "
            "TankModuleParams without context: v210 adds "
            "FirmwareCommit, which only the posting pico knows, and it SHALL "
            "NOT be fabricated."
        )
