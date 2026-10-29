import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.local.control.all.tanks.state/001 */
export const Gw1LocalControlAllTanksState = semaStrEnum(
    'gw1.local.control.all.tanks.state',
    '001',
    ['Initializing', 'HpOnStoreOff', 'HpOnStoreCharge', 'HpOffStoreOff', 'HpOffStoreDischarge', 'Dormant'],
    'Initializing',
);
export type Gw1LocalControlAllTanksState = z.infer<typeof Gw1LocalControlAllTanksState>;
