import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.quantity/003 */
export const Gw1Quantity = semaStrEnum(
    'gw1.quantity',
    '003',
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
        'Irradiance',
        'Currency',
    ],
    'Unknown',
);
export type Gw1Quantity = z.infer<typeof Gw1Quantity>;
