import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.g.node.class/000 */
export const GwGNodeClass = semaStrEnum(
    'gw.g.node.class',
    '000',
    [
        'Unknown',
        'TerminalAsset',
        'ConnectivityNode',
        'LeafTransactiveNode',
        'MarketMaker',
        'Scada',
        'PriceForecastService',
        'WeatherForecastService',
    ],
    'Unknown',
);
export type GwGNodeClass = z.infer<typeof GwGNodeClass>;
