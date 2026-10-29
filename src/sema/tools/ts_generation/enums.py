"""Emit one ``enums/<Class>.ts`` per enum version in the closure.

The newest version in the DAG is the plain class name; every older
version is ``<Class><NNN>`` under ``enums/old_versions/``, the Python
runtime's rule. Every enum is built on ``enums/semaEnum.ts``, the
TypeScript counterpart of ``gw_str_enum.py``: a string enum accepts the
version's values and decodes a string it does not know to the schema's
``default``, so a value a later version appended reaches this version as
the default; a value that is not a string is rejected. An integer enum
does the same over the ``value_descriptions`` names mapped to their
integers, so a consumer reads ``.enum.Energized`` as it reads the Python
member. Each schema keeps ``.options`` and exposes ``.default``.

``enums.test.ts`` is emitted beside them: every value parses to itself,
an unknown value of the right primitive decodes to the default, the
wrong primitive fails, and the default is one of the values.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from sema.tools.runtime_generation.helpers import (
    class_name_for_node,
    integer_enum_member_name,
    load_schema_for_node,
    string_enum_member_name,
)
from sema.tools.ts_generation.formats import ts_literal


class EnumVersion:
    """One enum version as the emitter sees it."""

    def __init__(
        self,
        name: str,
        version: str,
        class_name: str,
        is_latest: bool,
        schema: dict[str, Any],
    ) -> None:
        self.name = name
        self.version = version
        self.class_name = class_name
        self.is_latest = is_latest
        self.schema = schema

    @property
    def is_integer(self) -> bool:
        return self.schema["type"] == "integer"

    @property
    def relative_path(self) -> Path:
        if self.is_latest:
            return Path("enums") / f"{self.class_name}.ts"
        return Path("enums") / "old_versions" / f"{self.class_name}.ts"

    def members(self) -> list[tuple[str, Any]]:
        """``(member name, wire value)`` per value, in schema order."""
        values = self.schema["enum"]
        if not self.is_integer:
            return [(string_enum_member_name(str(v)), v) for v in values]
        descriptions = self.schema.get("x-gridworks", {}).get("value_descriptions")
        if not isinstance(descriptions, dict):
            raise ValueError(
                f"Integer enum {self.name}:{self.version} requires "
                "x-gridworks.value_descriptions"
            )
        return [(integer_enum_member_name(v, descriptions), v) for v in values]


SEMA_ENUM_TS = """\
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
"""


def zod_enum_expression(enum: EnumVersion) -> str:
    if "default" not in enum.schema:
        raise ValueError(f"Enum {enum.name}:{enum.version} has no default")
    default = ts_literal(enum.schema["default"])
    identity = f"'{enum.name}', '{enum.version}'"
    if enum.is_integer:
        pairs = ", ".join(f"{name}: {value}" for name, value in enum.members())
        return f"semaIntEnum({identity}, {{ {pairs} }} as const, {default})"
    values = ", ".join(ts_literal(value) for _, value in enum.members())
    return f"semaStrEnum({identity}, [{values}], {default})"


def render_enum(enum: EnumVersion) -> str:
    schema = enum.schema
    if schema["type"] not in ("string", "integer"):
        raise ValueError(
            f"Unsupported enum schema type for {enum.name}: {schema['type']}"
        )
    c = enum.class_name
    base = "./semaEnum" if enum.is_latest else "../semaEnum"
    helper = "semaIntEnum" if enum.is_integer else "semaStrEnum"
    lines = [
        "import { z } from 'zod';",
        f"import {{ {helper} }} from '{base}';",
        "",
        f"/** Sema: {schema['$id']} */",
        f"export const {c} = {zod_enum_expression(enum)};",
        f"export type {c} = z.infer<typeof {c}>;",
    ]
    return "\n".join(lines) + "\n"


def render_enums_index(enums: list[EnumVersion]) -> str:
    latest = sorted((e for e in enums if e.is_latest), key=lambda e: e.class_name)
    lines = [f"export * from './{e.class_name}';" for e in latest]
    return "\n".join(lines) + "\n"


def render_enums_test(enums: list[EnumVersion]) -> str:
    enums = sorted(enums, key=lambda e: (e.name, e.version))
    imports: list[str] = []
    blocks: list[str] = []
    for e in enums:
        module = (
            f"./{e.class_name}" if e.is_latest else f"./old_versions/{e.class_name}"
        )
        imports.append(f"import {{ {e.class_name} }} from '{module}';")
        c = e.class_name
        unknown = "999" if e.is_integer else "'__not_a_value__'"
        wrong_kind = "'0'" if e.is_integer else "0"
        lines = [
            f"describe('{e.name} {e.version}', () => {{",
            "    it('accepts every value', () => {",
        ]
        for _, value in e.members():
            lit = ts_literal(value)
            lines.append(f"        expect({c}.parse({lit})).toBe({lit});")
        lines += [
            "    });",
            "    it('decodes an unknown value to the default', () => {",
            f"        expect({c}.parse({unknown})).toBe({c}.default);",
            "    });",
            "    it('rejects the wrong primitive', () => {",
            f"        expect({c}.safeParse({wrong_kind}).success).toBe(false);",
            "    });",
            "    it('names its default among its values', () => {",
            f"        expect({c}.options).toContain({c}.default);",
            "    });",
            "    it('knows its sema name and version', () => {",
            f"        expect({c}.enumName).toBe('{e.name}');",
            f"        expect({c}.enumVersion).toBe('{e.version}');",
            "    });",
            "});",
        ]
        blocks.append("\n".join(lines))
    header = (
        "/** GENERATED by sema from the enum definitions. */\n"
        "import { describe, expect, it } from 'vitest';\n" + "\n".join(imports)
    )
    return header + "\n\n" + "\n\n".join(blocks) + "\n"


def collect_enums(dag, seed) -> list[EnumVersion]:
    dag_max = dag.dag_max()
    enums: list[EnumVersion] = []
    for node in dag.topo_sort():
        if node[0] != "enum":
            continue
        _, name, version = node
        enums.append(
            EnumVersion(
                name=name,
                version=version,
                class_name=class_name_for_node(node, dag_max),
                is_latest=dag_max[("enum", name)] == version,
                schema=load_schema_for_node(node, seed),
            )
        )
    return enums


def generate_enums(target_root: Path, dag, seed) -> None:
    enums = collect_enums(dag, seed)
    enums_root = target_root / "enums"
    if enums_root.exists():
        shutil.rmtree(enums_root)
    (enums_root / "old_versions").mkdir(parents=True)
    (enums_root / "semaEnum.ts").write_text(SEMA_ENUM_TS)
    for e in enums:
        (target_root / e.relative_path).write_text(render_enum(e))
    (enums_root / "index.ts").write_text(render_enums_index(enums))
    (enums_root / "enums.test.ts").write_text(render_enums_test(enums))
