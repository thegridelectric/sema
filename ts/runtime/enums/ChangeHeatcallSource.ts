import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/change.heatcall.source/000 */
export const ChangeHeatcallSource = semaStrEnum(
    'change.heatcall.source',
    '000',
    ['SwitchToWallThermostat', 'SwitchToScada'],
    'SwitchToWallThermostat',
);
export type ChangeHeatcallSource = z.infer<typeof ChangeHeatcallSource>;
