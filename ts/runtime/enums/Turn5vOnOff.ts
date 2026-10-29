import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/turn.5v.on.off/000 */
export const Turn5vOnOff = semaStrEnum('turn.5v.on.off', '000', ['TurnOn', 'TurnOff'], 'TurnOn');
export type Turn5vOnOff = z.infer<typeof Turn5vOnOff>;
