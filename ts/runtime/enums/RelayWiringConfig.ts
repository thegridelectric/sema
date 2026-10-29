import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/relay.wiring.config/000 */
export const RelayWiringConfig = semaStrEnum(
    'relay.wiring.config',
    '000',
    ['NormallyClosed', 'NormallyOpen', 'DoubleThrow'],
    'NormallyClosed',
);
export type RelayWiringConfig = z.infer<typeof RelayWiringConfig>;
