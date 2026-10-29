import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.leaf.ally.buffer.only.state/001 */
export const Gw1LeafAllyBufferOnlyState = semaStrEnum(
    'gw1.leaf.ally.buffer.only.state',
    '001',
    ['Dormant', 'Initializing', 'HpOn', 'HpOff', 'HpOffNonElectricBackup'],
    'Dormant',
);
export type Gw1LeafAllyBufferOnlyState = z.infer<typeof Gw1LeafAllyBufferOnlyState>;
