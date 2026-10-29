import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/i2c.operation/001 */
export const I2cOperation = semaStrEnum(
    'i2c.operation',
    '001',
    ['ReadBit', 'WriteBit', 'ReadReg', 'WriteReg', 'WriteByte', 'ReadBytes'],
    'ReadBit',
);
export type I2cOperation = z.infer<typeof I2cOperation>;
