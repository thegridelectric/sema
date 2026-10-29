import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.main.auto.state/001 */
export const Gw1MainAutoState = semaStrEnum(
    'gw1.main.auto.state',
    '001',
    ['LocalControl', 'LeafTransactiveNode', 'Dormant'],
    'LocalControl',
);
export type Gw1MainAutoState = z.infer<typeof Gw1MainAutoState>;
