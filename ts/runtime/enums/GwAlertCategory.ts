import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.alert.category/000 */
export const GwAlertCategory = semaStrEnum(
    'gw.alert.category',
    '000',
    ['Unknown', 'House', 'Fleet', 'PlatformService'],
    'Unknown',
);
export type GwAlertCategory = z.infer<typeof GwAlertCategory>;
