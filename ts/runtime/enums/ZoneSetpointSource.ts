import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/zone.setpoint.source/000 */
export const ZoneSetpointSource = semaStrEnum('zone.setpoint.source', '000', ['FromThermostat', 'Learned'], 'Learned');
export type ZoneSetpointSource = z.infer<typeof ZoneSetpointSource>;
