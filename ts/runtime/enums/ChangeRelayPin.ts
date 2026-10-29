import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/change.relay.pin/000 */
export const ChangeRelayPin = semaStrEnum('change.relay.pin', '000', ['DeEnergize', 'Energize'], 'DeEnergize');
export type ChangeRelayPin = z.infer<typeof ChangeRelayPin>;
