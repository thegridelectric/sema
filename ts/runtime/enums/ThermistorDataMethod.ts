import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/thermistor.data.method/000 */
export const ThermistorDataMethod = semaStrEnum(
    'thermistor.data.method',
    '000',
    ['SimpleBeta', 'BetaWithExponentialAveraging'],
    'SimpleBeta',
);
export type ThermistorDataMethod = z.infer<typeof ThermistorDataMethod>;
