import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/zone.circuit.governance.state/000 */
export const ZoneCircuitGovernanceState = semaStrEnum(
    'zone.circuit.governance.state',
    '000',
    ['Dormant', 'StatRules', 'Off', 'ScadaThermostatic'],
    'Dormant',
);
export type ZoneCircuitGovernanceState = z.infer<typeof ZoneCircuitGovernanceState>;
