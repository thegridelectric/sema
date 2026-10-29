import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/relay.closed.or.open/000 */
export const RelayClosedOrOpen = semaStrEnum(
    'relay.closed.or.open',
    '000',
    ['RelayClosed', 'RelayOpen'],
    'RelayClosed',
);
export type RelayClosedOrOpen = z.infer<typeof RelayClosedOrOpen>;
