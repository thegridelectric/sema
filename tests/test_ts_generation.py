"""The TypeScript runtime generator: drift guard and the generated Vitest suite.

Both need the ``ts/`` lane installed (Node 22, ``npm install`` in ``ts/``);
a missing install fails with the fix named, since the committed TypeScript
runtime is as much a build product as the Python one.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
import yaml

from sema.tools.seed_requests import expand_all_registry_seed
from sema.tools.ts_generation.generate_runtime import generate_runtime_ts


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "indexes" / "public_registry.yaml"
TS_ROOT = REPO_ROOT / "ts"
RUNTIME_ROOT = TS_ROOT / "runtime"
PRETTIER = TS_ROOT / "node_modules" / ".bin" / "prettier"
VITEST = TS_ROOT / "node_modules" / ".bin" / "vitest"


def require_ts_lane() -> None:
    if shutil.which("node") is None or not PRETTIER.exists() or not VITEST.exists():
        pytest.fail(
            "the ts/ lane is not installed: with Node 22 on PATH run "
            "`npm install` in ts/ (see ts/README.md)"
        )


def generate_all(target: Path) -> None:
    registry = yaml.safe_load(REGISTRY_PATH.read_text())
    with tempfile.TemporaryDirectory() as tmp_name:
        seed = expand_all_registry_seed(Path(tmp_name), registry)
    generate_runtime_ts(target, seed, registry)
    subprocess.run(
        [
            str(PRETTIER),
            "--config",
            str(TS_ROOT / ".prettierrc"),
            "--write",
            str(target),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def relative_files(root: Path) -> set[Path]:
    return {p.relative_to(root) for p in root.rglob("*") if p.is_file()}


def test_generated_runtime_matches_committed_runtime(tmp_path: Path) -> None:
    require_ts_lane()
    generate_all(tmp_path)
    fresh = relative_files(tmp_path)
    committed = relative_files(RUNTIME_ROOT)
    assert fresh == committed, (
        f"ts/runtime file set is stale: run scripts/regenerate_runtime_ts.sh "
        f"(only committed: {sorted(map(str, committed - fresh))}; "
        f"only fresh: {sorted(map(str, fresh - committed))})"
    )
    for rel in sorted(fresh):
        assert (tmp_path / rel).read_text() == (RUNTIME_ROOT / rel).read_text(), (
            f"ts/runtime/{rel} is stale: run scripts/regenerate_runtime_ts.sh"
        )


def test_generated_vitest_suite_passes() -> None:
    require_ts_lane()
    result = subprocess.run(
        [str(VITEST), "run"],
        cwd=TS_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
