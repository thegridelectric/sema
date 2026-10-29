import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.dac.channel/000 */
export const I2cDacChannel = semaStrEnum('i2c.dac.channel', '000', ['A', 'B', 'C', 'D'], 'A');
export type I2cDacChannel = z.infer<typeof I2cDacChannel>;
