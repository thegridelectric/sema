import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/zone.call.source/000 */
export const ZoneCallSource = semaStrEnum('zone.call.source', '000', ['WallThermostat', 'Scada'], 'WallThermostat');
export type ZoneCallSource = z.infer<typeof ZoneCallSource>;
