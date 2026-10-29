import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.refrigerant.cycle/000 */
export const GwRefrigerantCycle = semaStrEnum('gw.refrigerant.cycle', '000', ['Single', 'Cascade'], 'Single');
export type GwRefrigerantCycle = z.infer<typeof GwRefrigerantCycle>;
