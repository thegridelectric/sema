#!/usr/bin/env bash
#
# Regenerate the in-repo TypeScript runtime (ts/runtime), format it with
# Prettier (the single source of style; the generator need not match it
# exactly), typecheck it and run its generated Vitest suite.
#
# Needs Node 22 with npm and `npm install` done in ts/.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "==> Regenerating ts/runtime"
uv run python scripts/regenerate_runtime_ts.py

cd ts
echo "==> prettier --write"
npm run --silent format
echo "==> tsc --noEmit"
npm run --silent typecheck
echo "==> vitest run"
npm run --silent test
echo "==> Done."
