import { z } from 'zod';
import { semaStrEnum } from './semaEnum';

/** Sema: https://schemas.electricity.works/enums/g.node.instance.transport/000 */
export const GNodeInstanceTransport = semaStrEnum(
    'g.node.instance.transport',
    '000',
    ['RabbitAmqp', 'RabbitMqtt'],
    'RabbitAmqp',
);
export type GNodeInstanceTransport = z.infer<typeof GNodeInstanceTransport>;
