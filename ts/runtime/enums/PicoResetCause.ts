import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/pico.reset.cause/000 */
export const PicoResetCause = semaStrEnum(
    'pico.reset.cause',
    '000',
    ['Unknown', 'PowerOn', 'Watchdog', 'SelfReset'],
    'Unknown',
);
export type PicoResetCause = z.infer<typeof PicoResetCause>;
