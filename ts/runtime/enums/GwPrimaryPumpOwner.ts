import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.primary.pump.owner/000 */
export const GwPrimaryPumpOwner = semaStrEnum('gw.primary.pump.owner', '000', ['HeatPump', 'Scada'], 'HeatPump');
export type GwPrimaryPumpOwner = z.infer<typeof GwPrimaryPumpOwner>;
