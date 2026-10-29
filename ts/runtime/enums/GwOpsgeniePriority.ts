import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.opsgenie.priority/000 */
export const GwOpsgeniePriority = semaStrEnum('gw.opsgenie.priority', '000', ['P1', 'P2', 'P3', 'P4', 'P5'], 'P5');
export type GwOpsgeniePriority = z.infer<typeof GwOpsgeniePriority>;
