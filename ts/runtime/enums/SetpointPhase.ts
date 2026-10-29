import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/setpoint.phase/000 */
export const SetpointPhase = semaStrEnum(
    'setpoint.phase',
    '000',
    ['Unknown', 'LastHeatCallEndTemp', 'SuspectZoneBelowSetpoint', 'SuspectZoneAboveSetpoint'],
    'Unknown',
);
export type SetpointPhase = z.infer<typeof SetpointPhase>;
