import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/sieg.loop.strategy/000 */
export const SiegLoopStrategy = semaStrEnum(
    'sieg.loop.strategy',
    '000',
    ['HoldFullSend', 'StratProtect', 'LwtControl'],
    'HoldFullSend',
);
export type SiegLoopStrategy = z.infer<typeof SiegLoopStrategy>;
