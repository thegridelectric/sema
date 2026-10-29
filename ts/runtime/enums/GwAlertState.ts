import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.alert.state/000 */
export const GwAlertState = semaStrEnum('gw.alert.state', '000', ['Firing', 'Resolved'], 'Firing');
export type GwAlertState = z.infer<typeof GwAlertState>;
