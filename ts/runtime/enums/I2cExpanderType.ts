import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.expander.type/000 */
export const I2cExpanderType = semaStrEnum('i2c.expander.type', '000', ['Tca9555', 'Pcf8575'], 'Tca9555');
export type I2cExpanderType = z.infer<typeof I2cExpanderType>;
