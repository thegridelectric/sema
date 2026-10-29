import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/hz.calc.method/001 */
export const HzCalcMethod = semaStrEnum(
    'hz.calc.method',
    '001',
    ['BasicExpWeightedAvg', 'BasicButterWorth', 'UniformWindow'],
    'BasicExpWeightedAvg',
);
export type HzCalcMethod = z.infer<typeof HzCalcMethod>;
