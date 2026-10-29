import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.heat.call.interpretation/000 */
export const Gw1HeatCallInterpretation = semaStrEnum(
    'gw1.heat.call.interpretation',
    '000',
    ['DigitalZeroIsActive', 'DigitalOneIsActive', 'GreaterThanThreshold'],
    'DigitalZeroIsActive',
);
export type Gw1HeatCallInterpretation = z.infer<typeof Gw1HeatCallInterpretation>;
