import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.nolan.lc.buffer.only.state/000 */
export const Gw1NolanLcBufferOnlyState = semaStrEnum(
    'gw1.nolan.lc.buffer.only.state',
    '000',
    ['Initializing', 'HpCallOn', 'HpCallOff', 'Dormant'],
    'Initializing',
);
export type Gw1NolanLcBufferOnlyState = z.infer<typeof Gw1NolanLcBufferOnlyState>;
