import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.unit/000 */
export const Gw1Unit000 = semaStrEnum(
    'gw1.unit',
    '000',
    ['Unknown', 'Unitless', 'FahrenheitX100', 'Watts', 'WattHours', 'Gallons', 'GpmX100'],
    'Unknown',
);
export type Gw1Unit000 = z.infer<typeof Gw1Unit000>;
