import { z } from 'zod';
import { semaStrEnum } from '../semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.house.alert.kind/000 */
export const GwHouseAlertKind000 = semaStrEnum(
    'gw.house.alert.kind',
    '000',
    [
        'Unknown',
        'NoData',
        'ScadaRebootLoop',
        'CriticalGlitch',
        'ZoneBelowSetpoint',
        'ZoneFreezeRisk',
        'NoDistFlow',
        'NoStoreFlow',
        'HpNotResponding',
        'HpRunningOnpeak',
        'LocalControlActive',
    ],
    'Unknown',
);
export type GwHouseAlertKind000 = z.infer<typeof GwHouseAlertKind000>;
