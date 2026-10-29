import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/zone.call.circuit.state/000 */
export const ZoneCallCircuitState = semaStrEnum(
    'zone.call.circuit.state',
    '000',
    ['Dormant', 'Released', 'TakingHold', 'Held', 'StartingCall', 'Calling', 'StoppingCall', 'Releasing'],
    'Released',
);
export type ZoneCallCircuitState = z.infer<typeof ZoneCallCircuitState>;
