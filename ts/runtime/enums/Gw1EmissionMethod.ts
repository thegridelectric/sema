import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.emission.method/000 */
export const Gw1EmissionMethod = semaStrEnum(
    'gw1.emission.method',
    '000',
    ['OnTrigger', 'Periodic', 'AsyncAndPeriodic'],
    'OnTrigger',
);
export type Gw1EmissionMethod = z.infer<typeof Gw1EmissionMethod>;
