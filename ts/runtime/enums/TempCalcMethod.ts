import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/temp.calc.method/000 */
export const TempCalcMethod = semaStrEnum('temp.calc.method', '000', ['SimpleBetaForPico', 'SimpleBeta'], 'SimpleBeta');
export type TempCalcMethod = z.infer<typeof TempCalcMethod>;
