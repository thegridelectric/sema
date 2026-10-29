import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/market.type.name/000 */
export const MarketTypeName = semaStrEnum(
    'market.type.name',
    '000',
    ['unknown', 'rt5gate5', 'rt60gate5', 'da60', 'rt60gate30', 'rt15gate5', 'rt30gate5', 'rt60gate30b'],
    'unknown',
);
export type MarketTypeName = z.infer<typeof MarketTypeName>;
