import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/change.valve.state/000 */
export const ChangeValveState = semaStrEnum('change.valve.state', '000', ['OpenValve', 'CloseValve'], 'OpenValve');
export type ChangeValveState = z.infer<typeof ChangeValveState>;
