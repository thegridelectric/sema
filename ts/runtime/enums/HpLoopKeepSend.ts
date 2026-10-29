import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/hp.loop.keep.send/000 */
export const HpLoopKeepSend = semaStrEnum('hp.loop.keep.send', '000', ['SendLess', 'SendMore'], 'SendMore');
export type HpLoopKeepSend = z.infer<typeof HpLoopKeepSend>;
