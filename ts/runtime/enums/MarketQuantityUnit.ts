import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/market.quantity.unit/000 */
export const MarketQuantityUnit = semaStrEnum('market.quantity.unit', '000', ['AvgMW', 'AvgkW'], 'AvgMW');
export type MarketQuantityUnit = z.infer<typeof MarketQuantityUnit>;
