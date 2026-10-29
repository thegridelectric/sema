import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/day.of.week/000 */
export const DayOfWeek = semaStrEnum(
    'day.of.week',
    '000',
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'Monday',
);
export type DayOfWeek = z.infer<typeof DayOfWeek>;
