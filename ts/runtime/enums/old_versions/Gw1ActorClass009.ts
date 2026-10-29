import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.actor.class/009 */
export const Gw1ActorClass009 = semaStrEnum(
    'gw1.actor.class',
    '009',
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
    ],
    'NoActor',
);
export type Gw1ActorClass009 = z.infer<typeof Gw1ActorClass009>;
