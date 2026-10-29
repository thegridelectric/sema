import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/change.relay.state/000 */
export const ChangeRelayState = semaStrEnum('change.relay.state', '000', ['CloseRelay', 'OpenRelay'], 'OpenRelay');
export type ChangeRelayState = z.infer<typeof ChangeRelayState>;
