import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/thermostat.kind/000 */
export const ThermostatKind = semaStrEnum(
    'thermostat.kind',
    '000',
    ['MechanicalDial', 'HoneywellViaHubitat'],
    'MechanicalDial',
);
export type ThermostatKind = z.infer<typeof ThermostatKind>;
