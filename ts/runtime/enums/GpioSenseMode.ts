import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gpio.sense.mode/000 */
export const GpioSenseMode = semaStrEnum('gpio.sense.mode', '000', ['Polling', 'EdgeDetect'], 'Polling');
export type GpioSenseMode = z.infer<typeof GpioSenseMode>;
