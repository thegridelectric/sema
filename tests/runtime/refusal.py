"""Axiom refusal by mutation, for the registry's own runtime tests.

An axiom is proved by taking the type version's example, changing it so that
it violates one axiom clause and no other, and requiring the runtime to refuse
the result naming that axiom number (and clause label, when the axiom is
labeled). A structural error, or a refusal on another axiom, is a failure.
"""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from sema.runtime.base import SemaError, SemaType
from sema.runtime.codec import SemaCodec, default_codec

REPO_ROOT = Path(__file__).resolve().parents[2]
TYPES_DIR = REPO_ROOT / "definitions" / "types"

Payload = dict[str, Any]


def example(type_name: str, version: str | None = None) -> Payload:
    """The type version's first authored example, as a payload."""
    path = (
        TYPES_DIR / type_name / f"{version}.yaml"
        if version
        else TYPES_DIR / f"{type_name}.yaml"
    )
    schema = yaml.safe_load(path.read_text())
    return json.loads(schema["examples"][0])


def mutated(payload: Payload, mutate: Callable[[Payload], None]) -> Payload:
    """A deep copy of `payload` with `mutate` applied in place to the copy."""
    copied = copy.deepcopy(payload)
    mutate(copied)
    return copied


def runtime_class(
    type_name: str, version: str | None, codec: SemaCodec = default_codec
) -> type[SemaType]:
    """The generated class the codec decodes this type version with."""
    current = codec.registry[type_name]
    if version is None or version == current.version_value():
        return current
    return codec.old_versions[type_name][version]


CLAUSE_LINE = re.compile(r"^\s*([a-z])\.\s", re.MULTILINE)


def axioms(
    type_name: str, version: str | None = None, codec: SemaCodec = default_codec
) -> dict[int, list[str]]:
    """Axiom number -> clause labels (empty for an unlabeled axiom), read off
    the generated class: one `check_axiom_<n>` validator per axiom, clause
    labels from the statement in its docstring."""
    cls = runtime_class(type_name, version, codec)
    found: dict[int, list[str]] = {}
    for name in dir(cls):
        match = re.fullmatch(r"check_axiom_(\d+)", name)
        if match is None:
            continue
        doc = getattr(cls, name).__doc__ or ""
        found[int(match.group(1))] = CLAUSE_LINE.findall(doc)
    return dict(sorted(found.items()))


def assert_refused(
    codec: SemaCodec, payload: Payload, axiom: int, clause: str | None = None
) -> None:
    """The codec refuses `payload` at its own version, naming `axiom` (and
    `clause`). Accepting it, or refusing for any other reason, fails."""
    try:
        codec.from_dict(payload, mode="strict", auto_upgrade=False)
    except (SemaError, ValueError) as exc:
        said = str(exc)
    else:
        raise AssertionError(
            f"{payload.get('TypeName')} accepted a payload that violates axiom "
            f"{axiom}{' clause ' + clause if clause else ''}"
        )
    wants = [rf"Axiom {axiom}\b"]
    if clause is not None:
        wants.append(rf"clause {clause}\b")
    missing = [w for w in wants if re.search(w, said) is None]
    if missing:
        raise AssertionError(
            f"{payload.get('TypeName')} refused, but not on axiom {axiom}"
            f"{' clause ' + clause if clause else ''}: {said[:400]}"
        )
