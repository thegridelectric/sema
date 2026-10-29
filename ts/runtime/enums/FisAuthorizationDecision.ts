import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/fis.authorization.decision/000 */
export const FisAuthorizationDecision = semaStrEnum(
    'fis.authorization.decision',
    '000',
    ['Authorized', 'Denied'],
    'Denied',
);
export type FisAuthorizationDecision = z.infer<typeof FisAuthorizationDecision>;
