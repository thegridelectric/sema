import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.platform.alert.kind/000 */
export const GwPlatformAlertKind = semaStrEnum(
    'gw.platform.alert.kind',
    '000',
    ['Unknown', 'BrokerUnreachable'],
    'Unknown',
);
export type GwPlatformAlertKind = z.infer<typeof GwPlatformAlertKind>;
