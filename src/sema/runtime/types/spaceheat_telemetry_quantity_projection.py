from typing import Literal
from pydantic import model_validator
from sema.runtime.base import SemaType
from sema.runtime.enums import Gw1Quantity
from sema.runtime.enums import SpaceheatTelemetryName


_PROJECTION = {
    SpaceheatTelemetryName.Unknown: Gw1Quantity.Unknown,
    SpaceheatTelemetryName.PowerW: Gw1Quantity.Power,
    SpaceheatTelemetryName.WattHours: Gw1Quantity.Energy,
    SpaceheatTelemetryName.MilliWattHours: Gw1Quantity.Energy,
    SpaceheatTelemetryName.WaterTempCTimes1000: Gw1Quantity.Temperature,
    SpaceheatTelemetryName.WaterTempFTimes1000: Gw1Quantity.Temperature,
    SpaceheatTelemetryName.AirTempCTimes1000: Gw1Quantity.Temperature,
    SpaceheatTelemetryName.AirTempFTimes1000: Gw1Quantity.Temperature,
    SpaceheatTelemetryName.CelsiusTimes100: Gw1Quantity.Temperature,
    SpaceheatTelemetryName.GpmTimes100: Gw1Quantity.FlowRate,
    SpaceheatTelemetryName.GallonsTimes100: Gw1Quantity.Volume,
    SpaceheatTelemetryName.VoltageRmsMilliVolts: Gw1Quantity.Voltage,
    SpaceheatTelemetryName.VoltsTimesTen: Gw1Quantity.Voltage,
    SpaceheatTelemetryName.VoltsTimes100: Gw1Quantity.Voltage,
    SpaceheatTelemetryName.MicroVolts: Gw1Quantity.Voltage,
    SpaceheatTelemetryName.CurrentRmsMicroAmps: Gw1Quantity.Current,
    SpaceheatTelemetryName.HzTimes100: Gw1Quantity.Frequency,
    SpaceheatTelemetryName.MicroHz: Gw1Quantity.Frequency,
    SpaceheatTelemetryName.RelayState: Gw1Quantity.Unitless,
    SpaceheatTelemetryName.ThermostatState: Gw1Quantity.Unitless,
    SpaceheatTelemetryName.StorageLayer: Gw1Quantity.Unitless,
    SpaceheatTelemetryName.BinaryState: Gw1Quantity.Unitless,
    SpaceheatTelemetryName.PercentKeep: Gw1Quantity.Percent,
}


class SpaceheatTelemetryQuantityProjection(SemaType):
    """Sema: https://schemas.electricity.works/types/spaceheat.telemetry.quantity.projection/001"""

    telemetry_name: SpaceheatTelemetryName
    quantity: Gw1Quantity
    type_name: Literal["spaceheat.telemetry.quantity.projection"] = (
        "spaceheat.telemetry.quantity.projection"
    )
    version: Literal["001"] = "001"

    @classmethod
    def project(cls, telemetry_name: SpaceheatTelemetryName) -> Gw1Quantity:
        expected = _PROJECTION.get(telemetry_name)
        if expected is None:
            raise ValueError(
                f"No projection defined for telemetry_name {telemetry_name!r}."
            )
        return expected

    @model_validator(mode="after")
    def check_axiom_1(self) -> "SpaceheatTelemetryQuantityProjection":
        """
        Axiom 1: EnumeratedProjectionMapping
        Every (TelemetryName, Quantity) pair SHALL match the mapping declared in
        x-gridworks.projection.table. Any other combination is invalid.
        """
        expected = self.project(self.telemetry_name)
        if expected != self.quantity:
            raise ValueError(
                "Axiom 1 failed: telemetry_name and quantity do not match the enumerated projection."
            )
        return self
