import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.mux.type/000 */
export const I2cMuxType = semaStrEnum('i2c.mux.type', '000', ['Tca9548a'], 'Tca9548a');
export type I2cMuxType = z.infer<typeof I2cMuxType>;
