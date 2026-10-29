import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.actor.class/011 */
export const Gw1ActorClass011 = semaStrEnum(
    'gw1.actor.class',
    '011',
    [
        'NoActor',
        'PrimaryScada',
        'SecondaryScada',
        'PowerMeter',
        'LocalControl',
        'LeafAlly',
        'DerivedGenerator',
        'PicoCycler',
        'HpBoss',
        'I2cRelayMultiplexer',
        'I2cZeroTenMultiplexer',
        'Hubitat',
        'Relay',
        'MultipurposeSensor',
        'HoneywellThermostat',
        'ApiTankModule',
        'ApiFlowModule',
        'ZeroTenOutputer',
        'ApiBtuMeter',
        'SiegLoop',
        'GpioSensor',
        'I2cBus',
        'I2cRelayBoard',
        'I2cThermistorReader',
    ],
    'NoActor',
);
export type Gw1ActorClass011 = z.infer<typeof Gw1ActorClass011>;
