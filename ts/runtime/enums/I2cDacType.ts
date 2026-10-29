import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.dac.type/000 */
export const I2cDacType = semaStrEnum('i2c.dac.type', '000', ['Mcp4728', 'Mcp4725', 'Gp8403'], 'Mcp4728');
export type I2cDacType = z.infer<typeof I2cDacType>;
