import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.sim.device.type/000 */
export const Gw1SimDeviceType = semaStrEnum(
    'gw1.sim.device.type',
    '000',
    [
        'SimSensor',
        'SimPowerMeter',
        'SimGw108',
        'SimSamsungAE055FEYMCG',
        'SimHpOdu',
        'SimHpIdu',
        'SimKridaDoubleRelayBoard16',
    ],
    'SimSensor',
);
export type Gw1SimDeviceType = z.infer<typeof Gw1SimDeviceType>;
