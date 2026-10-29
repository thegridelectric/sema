import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.experiment.verdict/000 */
export const GwExperimentVerdict = semaStrEnum(
    'gw.experiment.verdict',
    '000',
    ['Unknown', 'Pass', 'Fail', 'Inconclusive'],
    'Unknown',
);
export type GwExperimentVerdict = z.infer<typeof GwExperimentVerdict>;
