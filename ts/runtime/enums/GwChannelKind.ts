import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.channel.kind/000 */
export const GwChannelKind = semaStrEnum(
    'gw.channel.kind',
    '000',
    [
        'Unknown',
        'DataChannel',
        'DerivedChannel',
        'StateMachine',
        'HeatCallSynth',
        'WeatherForecast',
        'WeatherObserved',
        'FloParams',
    ],
    'Unknown',
);
export type GwChannelKind = z.infer<typeof GwChannelKind>;
