import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/pico.cycler.event/000 */
export const PicoCyclerEvent = semaStrEnum(
    'pico.cycler.event',
    '000',
    [
        'WakeUp',
        'GoDormant',
        'PicoMissing',
        'ConfirmOpened',
        'StartClosing',
        'ConfirmClosed',
        'ConfirmRebooted',
        'ShakeZombies',
        'RebootDud',
        'Startup',
    ],
    'WakeUp',
);
export type PicoCyclerEvent = z.infer<typeof PicoCyclerEvent>;
