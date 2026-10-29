import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/reboot.picos/000 */
export const RebootPicos = semaStrEnum('reboot.picos', '000', ['RebootPicos'], 'RebootPicos');
export type RebootPicos = z.infer<typeof RebootPicos>;
