import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.dac.vref/000 */
export const I2cDacVref = semaStrEnum('i2c.dac.vref', '000', ['Internal', 'Vdd'], 'Internal');
export type I2cDacVref = z.infer<typeof I2cDacVref>;
