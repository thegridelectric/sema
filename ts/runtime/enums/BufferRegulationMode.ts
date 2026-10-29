import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/buffer.regulation.mode/000 */
export const BufferRegulationMode = semaStrEnum('buffer.regulation.mode', '000', ['Normal', 'Tight'], 'Normal');
export type BufferRegulationMode = z.infer<typeof BufferRegulationMode>;
