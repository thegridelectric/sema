import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.quantity/000 */
export const Gw1Quantity000 = semaStrEnum(
    'gw1.quantity',
    '000',
    [
        'Unknown',
        'Unitless',
        'Power',
        'Energy',
        'Temperature',
        'FlowRate',
        'Volume',
        'Voltage',
        'Current',
        'Percent',
        'Frequency',
    ],
    'Unknown',
);
export type Gw1Quantity000 = z.infer<typeof Gw1Quantity000>;
