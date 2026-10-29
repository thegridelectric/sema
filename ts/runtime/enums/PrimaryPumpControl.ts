import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/primary.pump.control/000 */
export const PrimaryPumpControl = semaStrEnum('primary.pump.control', '000', ['HeatPump', 'Scada'], 'HeatPump');
export type PrimaryPumpControl = z.infer<typeof PrimaryPumpControl>;
