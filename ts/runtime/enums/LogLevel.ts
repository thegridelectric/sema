import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/log.level/000 */
export const LogLevel = semaStrEnum(
    'log.level',
    '000',
    ['Critical', 'Error', 'Warning', 'Info', 'Debug', 'Trace'],
    'Info',
);
export type LogLevel = z.infer<typeof LogLevel>;
