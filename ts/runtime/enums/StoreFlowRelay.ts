import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/store.flow.relay/000 */
export const StoreFlowRelay = semaStrEnum(
    'store.flow.relay',
    '000',
    ['DischargingStore', 'ChargingStore'],
    'DischargingStore',
);
export type StoreFlowRelay = z.infer<typeof StoreFlowRelay>;
