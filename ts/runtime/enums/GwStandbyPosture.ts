import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.standby.posture/000 */
export const GwStandbyPosture = semaStrEnum(
    'gw.standby.posture',
    '000',
    ['MonitorOnly', 'NoHeatingOrCooling'],
    'MonitorOnly',
);
export type GwStandbyPosture = z.infer<typeof GwStandbyPosture>;
