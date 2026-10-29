import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/spruce.hack.hp.state/000 */
export const SpruceHackHpState = semaStrEnum(
    'spruce.hack.hp.state',
    '000',
    ['Unknown', 'HpDetectedOn', 'HpDetectedOff'],
    'Unknown',
);
export type SpruceHackHpState = z.infer<typeof SpruceHackHpState>;
