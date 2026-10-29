import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/fis.authorization.reason/000 */
export const FisAuthorizationReason = semaStrEnum(
    'fis.authorization.reason',
    '000',
    [
        'MalformedRequest',
        'PrincipalNotFound',
        'PrincipalSuspended',
        'RunOutsideUniverse',
        'NotInRegistry',
        'AliasMismatch',
        'ClassMismatch',
        'InstanceRevoked',
        'KillUnconfirmed',
        'LeaseRace',
        'IdempotentReconnect',
        'Superseded',
    ],
    'MalformedRequest',
);
export type FisAuthorizationReason = z.infer<typeof FisAuthorizationReason>;
