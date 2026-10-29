import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gpm.from.hz.method/000 */
export const GpmFromHzMethod = semaStrEnum('gpm.from.hz.method', '000', ['Constant'], 'Constant');
export type GpmFromHzMethod = z.infer<typeof GpmFromHzMethod>;
