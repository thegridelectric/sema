import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.quantity/001 */
export const Gw1Quantity001 = semaStrEnum(
    'gw1.quantity',
    '001',
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
        'Time',
    ],
    'Unknown',
);
export type Gw1Quantity001 = z.infer<typeof Gw1Quantity001>;
