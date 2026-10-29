import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/relay.open.or.closed/000 */
export const RelayOpenOrClosed = semaStrEnum(
    'relay.open.or.closed',
    '000',
    ['RelayClosed', 'RelayOpen'],
    'RelayClosed',
);
export type RelayOpenOrClosed = z.infer<typeof RelayOpenOrClosed>;
