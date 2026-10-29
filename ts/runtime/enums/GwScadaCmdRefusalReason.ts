import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.scada.cmd.refusal.reason/000 */
export const GwScadaCmdRefusalReason = semaStrEnum(
    'gw.scada.cmd.refusal.reason',
    '000',
    ['Unknown', 'Busy', 'NotMyBoss', 'UnknownEvent', 'OutOfRange', 'NotAControlNode'],
    'Unknown',
);
export type GwScadaCmdRefusalReason = z.infer<typeof GwScadaCmdRefusalReason>;
