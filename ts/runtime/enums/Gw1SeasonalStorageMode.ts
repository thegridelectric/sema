import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.seasonal.storage.mode/000 */
export const Gw1SeasonalStorageMode = semaStrEnum(
    'gw1.seasonal.storage.mode',
    '000',
    ['AllTanks', 'BufferOnly'],
    'AllTanks',
);
export type Gw1SeasonalStorageMode = z.infer<typeof Gw1SeasonalStorageMode>;
