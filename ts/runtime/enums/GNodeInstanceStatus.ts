import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/g.node.instance.status/000 */
export const GNodeInstanceStatus = semaStrEnum(
    'g.node.instance.status',
    '000',
    ['Active', 'Revoked', 'Ended'],
    'Active',
);
export type GNodeInstanceStatus = z.infer<typeof GNodeInstanceStatus>;
