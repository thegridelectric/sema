from typing import Literal
from pydantic import StrictFloat, StrictInt, model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import PicoBoardVariant
from sema.runtime.property_format import FirmwareCommit
from sema.runtime.property_format import MacAddress
from sema.runtime.property_format import PositiveFloat
from sema.runtime.property_format import PositiveInt
from sema.runtime.property_format import SpaceheatName


class AsyncBtuParams(SemaType):
    """Sema: https://schemas.electricity.works/types/async.btu.params/110"""

    hw_uid: str
    actor_node_name: SpaceheatName
    flow_channel_name: SpaceheatName
    send_hz: bool
    read_ct_voltage: bool
    read_temps: bool
    hot_channel_name: SpaceheatName | None = None
    cold_channel_name: SpaceheatName | None = None
    ct_channel_name: SpaceheatName | None = None
    thermistor_beta: StrictInt | None = None
    capture_period_s: PositiveInt
    gallons_per_pulse: PositiveFloat
    async_capture_delta_gpm_x100: PositiveInt
    async_capture_delta_celsius_x100: PositiveInt | None = None
    async_capture_delta_ct_volts_x100: PositiveInt | None = None
    capture_offset_s: StrictFloat | None = None
    pico_board_variant: PicoBoardVariant
    micropython_version: str
    firmware_commit: FirmwareCommit
    mac_address: MacAddress
    type_name: Literal["async.btu.params"] = "async.btu.params"
    version: Literal["110"] = "110"

    @model_validator(mode="after")
    def check_axiom_1(self) -> "AsyncBtuParams":
        """
        Axiom 1: ReadCtVoltageIffCtChannelName
        ReadCtVoltage is true iff CtChannelName is present.
        """
        truthy = [
            bool(self.read_ct_voltage),
            self.ct_channel_name is not None,
        ]
        if not (all(truthy) or not any(truthy)):
            raise ValueError(
                "Axiom 1: ReadCtVoltage and CtChannelName must either BOTH be "
                "set/present (True/nonnull) or BOTH be unset/absent."
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> "AsyncBtuParams":
        """
        Axiom 2: ReadTempsIffTemperatureFields
        ReadTemps is true iff HotChannelName, ColdChannelName, ThermistorBeta
        and AsyncCaptureDeltaCelsiusX100 are all present; ReadTemps is false
        iff all four are absent.
        """
        present = [
            self.hot_channel_name is not None,
            self.cold_channel_name is not None,
            self.thermistor_beta is not None,
            self.async_capture_delta_celsius_x100 is not None,
        ]
        if self.read_temps and not all(present):
            raise ValueError(
                "Axiom 2: ReadTemps is true, so HotChannelName, ColdChannelName, "
                "ThermistorBeta and AsyncCaptureDeltaCelsiusX100 must all be present."
            )
        if not self.read_temps and any(present):
            raise ValueError(
                "Axiom 2: ReadTemps is false, so HotChannelName, ColdChannelName, "
                "ThermistorBeta and AsyncCaptureDeltaCelsiusX100 must all be absent."
            )
        return self
