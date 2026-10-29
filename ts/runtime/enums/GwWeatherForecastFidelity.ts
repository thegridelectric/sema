import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.weather.forecast.fidelity/000 */
export const GwWeatherForecastFidelity = semaStrEnum(
    'gw.weather.forecast.fidelity',
    '000',
    ['Unknown', 'Live', 'Stored', 'SeasonalTemplate'],
    'Unknown',
);
export type GwWeatherForecastFidelity = z.infer<typeof GwWeatherForecastFidelity>;
