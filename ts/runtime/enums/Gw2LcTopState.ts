import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw2.lc.top.state/000 */
export const Gw2LcTopState = semaStrEnum(
    'gw2.lc.top.state',
    '000',
    ['Dormant', 'Normal', 'ScadaBlind', 'Standby', 'InBackup', 'ColdOverride'],
    'Dormant',
);
export type Gw2LcTopState = z.infer<typeof Gw2LcTopState>;
