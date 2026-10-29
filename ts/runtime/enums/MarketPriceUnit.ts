import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/market.price.unit/000 */
export const MarketPriceUnit = semaStrEnum('market.price.unit', '000', ['USDPerMWh'], 'USDPerMWh');
export type MarketPriceUnit = z.infer<typeof MarketPriceUnit>;
