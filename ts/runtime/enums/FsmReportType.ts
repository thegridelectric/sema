import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/fsm.report.type/000 */
export const FsmReportType = semaStrEnum('fsm.report.type', '000', ['Other', 'Event', 'Action'], 'Other');
export type FsmReportType = z.infer<typeof FsmReportType>;
