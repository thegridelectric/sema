import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/zone.call.circuit.event/000 */
export const ZoneCallCircuitEvent = semaStrEnum(
    'zone.call.circuit.event',
    '000',
    [
        'WakeUp',
        'GoDormant',
        'Release',
        'ScadaHold',
        'ScadaCall',
        'ConfirmHeld',
        'ConfirmCalling',
        'ConfirmReleased',
        'ActuationFailed',
    ],
    'GoDormant',
);
export type ZoneCallCircuitEvent = z.infer<typeof ZoneCallCircuitEvent>;
