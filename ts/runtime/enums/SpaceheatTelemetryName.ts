import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/spaceheat.telemetry.name/007 */
export const SpaceheatTelemetryName = semaStrEnum(
    'spaceheat.telemetry.name',
    '007',
    [
        'Unknown',
        'PowerW',
        'RelayState',
        'WaterTempCTimes1000',
        'WaterTempFTimes1000',
        'GpmTimes100',
        'CurrentRmsMicroAmps',
        'GallonsTimes100',
        'VoltageRmsMilliVolts',
        'MilliWattHours',
        'MicroHz',
        'AirTempCTimes1000',
        'AirTempFTimes1000',
        'ThermostatState',
        'MicroVolts',
        'VoltsTimesTen',
        'WattHours',
        'StorageLayer',
        'PercentKeep',
        'CelsiusTimes100',
        'VoltsTimes100',
        'HzTimes100',
        'BinaryState',
    ],
    'Unknown',
);
export type SpaceheatTelemetryName = z.infer<typeof SpaceheatTelemetryName>;
