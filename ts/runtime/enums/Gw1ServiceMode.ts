import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.service.mode/000 */
export const Gw1ServiceMode = semaStrEnum('gw1.service.mode', '000', ['Heating', 'Cooling'], 'Heating');
export type Gw1ServiceMode = z.infer<typeof Gw1ServiceMode>;
