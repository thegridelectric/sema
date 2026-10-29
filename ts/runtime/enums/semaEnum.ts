/** The base of every generated enum, the counterpart of the Python
 *  runtime's GwStrEnum and SemaEnum: a schema that accepts the version's
 *  values and decodes a value of the right primitive it does not know to
 *  the version's default, so a value a later version appended reaches
 *  this version as the default rather than a rejection. A value of the
 *  wrong primitive is rejected. `.options` lists the values, `.default`
 *  is the default, `.enumName` and `.enumVersion` are the sema name and
 *  version, and an integer enum's `.enum` maps its names to its integers. */
import { z } from 'zod';

export function semaStrEnum<const T extends readonly [string, ...string[]]>(
    enumName: string,
    enumVersion: string,
    values: T,
    defaultValue: T[number],
) {
    const known = z.enum(values);
    const schema = z.preprocess(
        (v) => (typeof v === 'string' && !(values as readonly string[]).includes(v) ? defaultValue : v),
        known,
    );
    return Object.assign(schema, {
        options: known.options,
        enum: known.enum,
        default: defaultValue,
        enumName,
        enumVersion,
    });
}

export function semaIntEnum<const T extends Readonly<Record<string, number>>>(
    enumName: string,
    enumVersion: string,
    names: T,
    defaultValue: T[keyof T],
) {
    const known = z.enum(names);
    const values: readonly number[] = Object.values(names);
    const schema = z.preprocess(
        (v) => (typeof v === 'number' && Number.isInteger(v) && !values.includes(v) ? defaultValue : v),
        known,
    );
    return Object.assign(schema, {
        options: known.options,
        enum: known.enum,
        default: defaultValue,
        enumName,
        enumVersion,
    });
}
