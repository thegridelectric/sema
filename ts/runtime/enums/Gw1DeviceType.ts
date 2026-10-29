import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw1.device.type/000 */
export const Gw1DeviceType = semaStrEnum(
    'gw1.device.type',
    '000',
    [
        'EgaugePowerMeter',
        'GridworksTsnap1ScadaBoard',
        'HubitatC7Hub',
        'Amphenol10kThermistor',
        'OmegaFtb8010FlowMeter',
        'HoneywellT6Thermostat',
        'TewaThermistor',
        'EkmFlowMeter',
        'KridaDoubleRelayBoard16',
        'GridworksPicoFlowHall',
        'GridworksPicoFlowReed',
        'SaierFlowSensor',
        'DfrobotDualAnalogOut',
        'GridworksTankModule3',
        'Gw101',
        'Gw108RevB',
        'AbstractWebServer',
        'Gw108I2cRelay',
        'Gw108GpioRelay',
        'SamsungAE055FCYDCG',
        'SamsungAE055FEYMCG',
        'Gw108Adc',
        'MitsubishiWUZSA48NMZ',
        'MitsubishiERSFNM6E',
        'LGARUM048GSS5',
        'LGARNH423K3A4',
        'SamsungAM048TXMDCH',
        'SamsungAM048CNBFCB',
        'ArcticMAHRW030ZA',
    ],
    'EgaugePowerMeter',
);
export type Gw1DeviceType = z.infer<typeof Gw1DeviceType>;
