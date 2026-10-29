import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.fleet.alert.kind/000 */
export const GwFleetAlertKind = semaStrEnum('gw.fleet.alert.kind', '000', ['Unknown', 'AllHousesSilent'], 'Unknown');
export type GwFleetAlertKind = z.infer<typeof GwFleetAlertKind>;
