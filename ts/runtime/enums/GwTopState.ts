import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.top.state/000 */
export const GwTopState = semaStrEnum('gw.top.state', '000', ['Auto', 'Admin'], 'Auto');
export type GwTopState = z.infer<typeof GwTopState>;
