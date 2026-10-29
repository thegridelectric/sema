import { z } from 'zod';
import { semaIntEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/relay.energization.state/000 */
export const RelayEnergizationState = semaIntEnum(
    'relay.energization.state',
    '000',
    { DeEnergized: 0, Energized: 1 } as const,
    0,
);
export type RelayEnergizationState = z.infer<typeof RelayEnergizationState>;
