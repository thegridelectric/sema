import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/single.pico.state/000 */
export const SinglePicoState = semaStrEnum('single.pico.state', '000', ['Alive', 'Flatlined', 'Zombie'], 'Flatlined');
export type SinglePicoState = z.infer<typeof SinglePicoState>;
