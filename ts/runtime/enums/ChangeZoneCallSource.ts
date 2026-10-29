import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/change.zone.call.source/000 */
export const ChangeZoneCallSource = semaStrEnum(
    'change.zone.call.source',
    '000',
    ['SwitchToWallThermostat', 'SwitchToScada'],
    'SwitchToWallThermostat',
);
export type ChangeZoneCallSource = z.infer<typeof ChangeZoneCallSource>;
