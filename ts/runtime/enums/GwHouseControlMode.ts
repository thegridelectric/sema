import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.house.control.mode/000 */
export const GwHouseControlMode = semaStrEnum(
    'gw.house.control.mode',
    '000',
    ['Unknown', 'LocalControl', 'Ltn', 'Admin'],
    'Unknown',
);
export type GwHouseControlMode = z.infer<typeof GwHouseControlMode>;
