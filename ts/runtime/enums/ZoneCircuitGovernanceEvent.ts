import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/zone.circuit.governance.event/000 */
export const ZoneCircuitGovernanceEvent = semaStrEnum(
    'zone.circuit.governance.event',
    '000',
    ['WakeUp', 'GoDormant', 'SwitchToStatRules', 'SwitchToOff', 'SwitchToThermostatic'],
    'GoDormant',
);
export type ZoneCircuitGovernanceEvent = z.infer<typeof ZoneCircuitGovernanceEvent>;
