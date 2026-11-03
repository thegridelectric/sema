#!/usr/bin/env bash
#
# Local gate for this repo. Sema has no GitHub workflow; run this before
# committing. When a workflow is added, call this script from it.
#
# Usage: ./ci.sh
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

step() { printf '\n=== %s ===\n' "$1"; shift; "$@"; }

step "uv sync (locked)" uv sync --all-groups --locked
step "ruff check" uv run ruff check --no-fix .
step "ruff format --check" uv run ruff format --check .
step "tests" uv run pytest -q

printf '\nAll checks passed.\n'
