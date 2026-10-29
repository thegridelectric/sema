import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.market.product.name/000 */
export const GwMarketProductName = semaStrEnum(
    'gw.market.product.name',
    '000',
    ['unknown', 'da60', 'rt60gate5', 'rt60gate30', 'rt60gate30b', 'rt30gate5', 'rt15gate5', 'rt5gate5'],
    'unknown',
);
export type GwMarketProductName = z.infer<typeof GwMarketProductName>;
