import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.slow.dispatch.contract.status/000 */
export const Gw1SlowDispatchContractStatus = semaStrEnum(
    'gw1.slow.dispatch.contract.status',
    '000',
    [
        'Unknown',
        'Created',
        'Received',
        'Confirmed',
        'Active',
        'TerminatedByLtn',
        'TerminatedByScada',
        'CompletedUnknownOutcome',
        'CompletedSuccess',
        'CompletedFailureByScada',
        'CompletedFailureByLtn',
    ],
    'Unknown',
);
export type Gw1SlowDispatchContractStatus = z.infer<typeof Gw1SlowDispatchContractStatus>;
