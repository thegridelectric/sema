import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/heat.pump.control/000 */
export const HeatPumpControl = semaStrEnum(
    'heat.pump.control',
    '000',
    ['BufferTankAquastat', 'Scada'],
    'BufferTankAquastat',
);
export type HeatPumpControl = z.infer<typeof HeatPumpControl>;
