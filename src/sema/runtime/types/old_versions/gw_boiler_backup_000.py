from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.property_format import SpaceheatName
from sema.runtime.types.gw_boiler_backup import GwBoilerBackup


class GwBoilerBackup000(SemaType):
    """Sema: https://schemas.electricity.works/types/gw.boiler.backup/000"""

    failsafe_relay_name: SpaceheatName
    aquastat_ctrl_relay_name: SpaceheatName
    in_service: bool
    type_name: Literal["gw.boiler.backup"] = "gw.boiler.backup"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "GwBoilerBackup000":
        """
        Axiom 1: DistinctRelays
        FailsafeRelayName SHALL NOT equal AquastatCtrlRelayName.
        """
        if self.failsafe_relay_name == self.aquastat_ctrl_relay_name:
            raise ValueError(
                "Axiom 1 (DistinctRelays) failed: FailsafeRelayName and "
                f"AquastatCtrlRelayName are both {self.failsafe_relay_name}."
            )
        return self

    def upgrade(self) -> GwBoilerBackup:
        """
        - FailsafeRelayName becomes optional
        - AquastatCtrlRelayName becomes InterceptRelayName
        """
        data = self.model_dump()
        data["version"] = "001"
        data["intercept_relay_name"] = data.pop("aquastat_ctrl_relay_name")
        return GwBoilerBackup.model_validate(data)
