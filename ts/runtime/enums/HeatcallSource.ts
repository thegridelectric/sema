import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/heatcall.source/000 */
export const HeatcallSource = semaStrEnum('heatcall.source', '000', ['WallThermostat', 'Scada'], 'WallThermostat');
export type HeatcallSource = z.infer<typeof HeatcallSource>;
