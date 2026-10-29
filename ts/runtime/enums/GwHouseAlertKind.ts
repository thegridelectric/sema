import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/gw.house.alert.kind/001 */
export const GwHouseAlertKind = semaStrEnum(
    'gw.house.alert.kind',
    '001',
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
        'ScadaSilent',
        'LtnSilent',
    ],
    'Unknown',
);
export type GwHouseAlertKind = z.infer<typeof GwHouseAlertKind>;
