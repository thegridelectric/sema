import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.quantity/002 */
export const Gw1Quantity002 = semaStrEnum(
    'gw1.quantity',
    '002',
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
        'WindSpeed',
    ],
    'Unknown',
);
export type Gw1Quantity002 = z.infer<typeof Gw1Quantity002>;
