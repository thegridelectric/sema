import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.primary.flow.source/000 */
export const GwPrimaryFlowSource = semaStrEnum(
    'gw.primary.flow.source',
    '000',
    ['Measured', 'DerivedSiegSum'],
    'Measured',
);
export type GwPrimaryFlowSource = z.infer<typeof GwPrimaryFlowSource>;
