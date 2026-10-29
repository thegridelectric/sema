import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.system.mode/000 */
export const Gw1SystemMode = semaStrEnum('gw1.system.mode', '000', ['Heating', 'Standby', 'MonitorOnly'], 'Heating');
export type Gw1SystemMode = z.infer<typeof Gw1SystemMode>;
