import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/spaceheat.unit/001 */
export const SpaceheatUnit = semaStrEnum(
    'spaceheat.unit',
    '001',
    [
        'Unknown',
        'Unitless',
        'W',
        'Celcius',
        'Fahrenheit',
        'Gpm',
        'WattHours',
        'AmpsRms',
        'VoltsRms',
        'Gallons',
        'ThermostatStateEnum',
    ],
    'Unknown',
);
export type SpaceheatUnit = z.infer<typeof SpaceheatUnit>;
