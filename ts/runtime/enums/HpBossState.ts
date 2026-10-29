import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/hp.boss.state/000 */
export const HpBossState = semaStrEnum('hp.boss.state', '000', ['PreparingToTurnOn', 'HpOn', 'HpOff'], 'HpOff');
export type HpBossState = z.infer<typeof HpBossState>;
