import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.opsgenie.alert.status/000 */
export const GwOpsgenieAlertStatus = semaStrEnum('gw.opsgenie.alert.status', '000', ['Open', 'Closed'], 'Open');
export type GwOpsgenieAlertStatus = z.infer<typeof GwOpsgenieAlertStatus>;
