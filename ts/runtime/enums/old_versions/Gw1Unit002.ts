import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.unit/002 */
export const Gw1Unit002 = semaStrEnum(
    'gw1.unit',
    '002',
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
    ],
    'Unknown',
);
export type Gw1Unit002 = z.infer<typeof Gw1Unit002>;
