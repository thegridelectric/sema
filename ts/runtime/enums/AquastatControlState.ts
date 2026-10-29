import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/aquastat.control.state/000 */
export const AquastatControlState = semaStrEnum('aquastat.control.state', '000', ['Boiler', 'Scada'], 'Boiler');
export type AquastatControlState = z.infer<typeof AquastatControlState>;
