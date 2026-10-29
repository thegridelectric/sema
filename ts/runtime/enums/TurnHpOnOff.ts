import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/turn.hp.on.off/000 */
export const TurnHpOnOff = semaStrEnum('turn.hp.on.off', '000', ['TurnOn', 'TurnOff'], 'TurnOn');
export type TurnHpOnOff = z.infer<typeof TurnHpOnOff>;
