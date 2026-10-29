import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.actor.class/013 */
export const Gw1ActorClass013 = semaStrEnum(
    'gw1.actor.class',
    '013',
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
        'SimSensorActor',
        'SimRelayActor',
        'I2cDacWriter',
        'HpTwin',
    ],
    'NoActor',
);
export type Gw1ActorClass013 = z.infer<typeof Gw1ActorClass013>;
