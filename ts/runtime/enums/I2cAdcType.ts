import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.adc.type/000 */
export const I2cAdcType = semaStrEnum('i2c.adc.type', '000', ['Ads1115', 'Ads1015'], 'Ads1115');
export type I2cAdcType = z.infer<typeof I2cAdcType>;
