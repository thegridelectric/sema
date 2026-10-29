import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/sieg.valve.state/000 */
export const SiegValveState = semaStrEnum(
    'sieg.valve.state',
    '000',
    ['FullySend', 'FullyKeep', 'KeepingMore', 'KeepingLess', 'SteadyBlend'],
    'FullySend',
);
export type SiegValveState = z.infer<typeof SiegValveState>;
