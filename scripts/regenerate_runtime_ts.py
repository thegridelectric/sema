from __future__ import annotations

import tempfile
from pathlib import Path

import yaml

from sema.tools.build_public_registry import build as build_public_registry
from sema.tools.schema_validation import validate_definitions
from sema.tools.seed_requests import expand_all_registry_seed
from sema.tools.ts_generation.generate_runtime import generate_runtime_ts


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "indexes" / "public_registry.yaml"
RUNTIME_ROOT = REPO_ROOT / "ts" / "runtime"


def main() -> None:
    findings = validate_definitions(REPO_ROOT / "definitions")
    if findings:
        raise SystemExit(
            "Refusing to generate: schema files violate the JSON Schema "
            "2020-12 metaschema:\n" + "\n".join(findings)
        )
    build_public_registry()
    registry = yaml.safe_load(REGISTRY_PATH.read_text())
    with tempfile.TemporaryDirectory() as tmp_name:
        seed = expand_all_registry_seed(Path(tmp_name), registry)
    generate_runtime_ts(RUNTIME_ROOT, seed, registry)
    print(f"Regenerated TypeScript runtime at {RUNTIME_ROOT}")


if __name__ == "__main__":
    main()
