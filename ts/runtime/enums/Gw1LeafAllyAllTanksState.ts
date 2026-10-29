import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.leaf.ally.all.tanks.state/001 */
export const Gw1LeafAllyAllTanksState = semaStrEnum(
    'gw1.leaf.ally.all.tanks.state',
    '001',
    [
        'Dormant',
        'Initializing',
        'HpOnStoreOff',
        'HpOnStoreCharge',
        'HpOffStoreOff',
        'HpOffStoreDischarge',
        'HpOffNonElectricBackup',
    ],
    'Dormant',
);
export type Gw1LeafAllyAllTanksState = z.infer<typeof Gw1LeafAllyAllTanksState>;
