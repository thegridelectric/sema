import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.adc.channel/000 */
export const I2cAdcChannel = semaStrEnum('i2c.adc.channel', '000', ['P0', 'P1', 'P2', 'P3'], 'P0');
export type I2cAdcChannel = z.infer<typeof I2cAdcChannel>;
