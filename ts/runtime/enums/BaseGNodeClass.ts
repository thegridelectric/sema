import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/base.g.node.class/000 */
export const BaseGNodeClass = semaStrEnum(
    'base.g.node.class',
    '000',
    ['TerminalAsset', 'LeafTransactiveNode', 'ConnectivityNode', 'MarketMaker', 'Logical'],
    'Logical',
);
export type BaseGNodeClass = z.infer<typeof BaseGNodeClass>;
