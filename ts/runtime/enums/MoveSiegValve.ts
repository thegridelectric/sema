import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/move.sieg.valve/001 */
export const MoveSiegValve = semaStrEnum(
    'move.sieg.valve',
    '001',
    ['MoveToFullSend', 'MoveToFullKeep', 'StopValve'],
    'MoveToFullSend',
);
export type MoveSiegValve = z.infer<typeof MoveSiegValve>;
