import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/pico.board.variant/000 */
export const PicoBoardVariant = semaStrEnum(
    'pico.board.variant',
    '000',
    ['Unknown', 'PicoWiznetEth2040', 'PicoWiznetEth2350', 'PicoRaspberryWifi2040'],
    'Unknown',
);
export type PicoBoardVariant = z.infer<typeof PicoBoardVariant>;
