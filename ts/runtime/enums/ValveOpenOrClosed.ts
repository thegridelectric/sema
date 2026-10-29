import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/valve.open.or.closed/000 */
export const ValveOpenOrClosed = semaStrEnum('valve.open.or.closed', '000', ['ValveOpen', 'ValveClosed'], 'ValveOpen');
export type ValveOpenOrClosed = z.infer<typeof ValveOpenOrClosed>;
