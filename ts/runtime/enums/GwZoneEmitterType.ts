import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.zone.emitter.type/000 */
export const GwZoneEmitterType = semaStrEnum(
    'gw.zone.emitter.type',
    '000',
    ['Other', 'RadiantSlab', 'FanCoil'],
    'Other',
);
export type GwZoneEmitterType = z.infer<typeof GwZoneEmitterType>;
