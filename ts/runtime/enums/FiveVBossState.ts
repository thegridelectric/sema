import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/five.v.boss.state/000 */
export const FiveVBossState = semaStrEnum(
    'five.v.boss.state',
    '000',
    ['PicoCycler', 'TurningOff', 'FiveVOff', 'TurningOn'],
    'PicoCycler',
);
export type FiveVBossState = z.infer<typeof FiveVBossState>;
