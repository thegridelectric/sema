import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.lc.top.state/001 */
export const Gw1LcTopState = semaStrEnum(
    'gw1.lc.top.state',
    '001',
    ['Dormant', 'UsingNonElectricBackup', 'Normal', 'ScadaBlind', 'Monitor'],
    'Dormant',
);
export type Gw1LcTopState = z.infer<typeof Gw1LcTopState>;
