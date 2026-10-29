"""Generate the TypeScript runtime for a seed: the stages in dependency order."""

from __future__ import annotations

from pathlib import Path

from sema.tools.build_seed_dag import build_seed_dag_from_data
from sema.tools.ts_generation.enums import generate_enums
from sema.tools.ts_generation.formats import generate_formats


def generate_runtime_ts(target_root: Path, seed: dict, registry: dict) -> None:
    dag = build_seed_dag_from_data(seed, registry)
    target_root.mkdir(parents=True, exist_ok=True)
    generate_formats(target_root, dag, seed)
    generate_enums(target_root, dag, seed)
