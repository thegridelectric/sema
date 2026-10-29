import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.dispatch.refusal.reason/000 */
export const GwDispatchRefusalReason = semaStrEnum(
    'gw.dispatch.refusal.reason',
    '000',
    ['NoTaDeed', 'OperatorHold', 'ServiceContractBroken', 'ScadaBlind', 'InAdmin'],
    'OperatorHold',
);
export type GwDispatchRefusalReason = z.infer<typeof GwDispatchRefusalReason>;
