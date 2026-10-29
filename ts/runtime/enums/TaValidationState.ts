import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/ta.validation.state/000 */
export const TaValidationState = semaStrEnum(
    'ta.validation.state',
    '000',
    ['UnValidated', 'ValidatedRealAssetAndGps', 'ValidatedRealAssetIncorrectGps', 'ValidatedSimulatedAsset'],
    'UnValidated',
);
export type TaValidationState = z.infer<typeof TaValidationState>;
