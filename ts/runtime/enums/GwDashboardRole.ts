import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.dashboard.role/000 */
export const GwDashboardRole = semaStrEnum('gw.dashboard.role', '000', ['Admin', 'Owner', 'Viewer'], 'Viewer');
export type GwDashboardRole = z.infer<typeof GwDashboardRole>;
