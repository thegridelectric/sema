import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.unit/003 */
export const Gw1Unit = semaStrEnum(
    'gw1.unit',
    '003',
    [
        'Unknown',
        'Unitless',
        'FahrenheitX100',
        'Watts',
        'WattHours',
        'Gallons',
        'GpmX100',
        'Seconds',
        'SecondsX10',
        'Milliseconds',
        'DollarsX1000',
        'MilesPerHourX1000',
        'KilowattHoursX1000',
        'WattsPerSquareMeter',
        'MilesPerHourX10',
        'FahrenheitX10',
    ],
    'Unknown',
);
export type Gw1Unit = z.infer<typeof Gw1Unit>;
