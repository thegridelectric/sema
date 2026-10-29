import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/g.node.status/000 */
export const GNodeStatus = semaStrEnum(
    'g.node.status',
    '000',
    ['Pending', 'Active', 'Suspended', 'PermanentlyDeactivated'],
    'Pending',
);
export type GNodeStatus = z.infer<typeof GNodeStatus>;
