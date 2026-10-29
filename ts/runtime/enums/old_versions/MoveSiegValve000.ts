import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/move.sieg.valve/000 */
export const MoveSiegValve000 = semaStrEnum(
    'move.sieg.valve',
    '000',
    ['MoveToFullSend', 'MoveToFullKeep'],
    'MoveToFullSend',
);
export type MoveSiegValve000 = z.infer<typeof MoveSiegValve000>;
