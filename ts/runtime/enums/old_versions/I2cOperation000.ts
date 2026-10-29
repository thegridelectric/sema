import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.operation/000 */
export const I2cOperation000 = semaStrEnum(
    'i2c.operation',
    '000',
    ['ReadBit', 'WriteBit', 'ReadReg', 'WriteReg'],
    'ReadBit',
);
export type I2cOperation000 = z.infer<typeof I2cOperation000>;
