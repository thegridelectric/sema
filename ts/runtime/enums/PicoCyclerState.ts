import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/pico.cycler.state/000 */
export const PicoCyclerState = semaStrEnum(
    'pico.cycler.state',
    '000',
    ['Dormant', 'PicosLive', 'RelayOpening', 'RelayOpen', 'RelayClosing', 'PicosRebooting', 'AllZombies'],
    'PicosLive',
);
export type PicoCyclerState = z.infer<typeof PicoCyclerState>;
