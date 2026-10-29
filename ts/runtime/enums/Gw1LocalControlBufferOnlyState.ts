import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.local.control.buffer.only.state/001 */
export const Gw1LocalControlBufferOnlyState = semaStrEnum(
    'gw1.local.control.buffer.only.state',
    '001',
    ['Initializing', 'HpOn', 'HpOff', 'Dormant'],
    'Initializing',
);
export type Gw1LocalControlBufferOnlyState = z.infer<typeof Gw1LocalControlBufferOnlyState>;
