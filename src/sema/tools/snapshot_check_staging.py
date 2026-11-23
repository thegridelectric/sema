"""Check a vendored Sema snapshot against the seed that is committed beside it.

Shipped into every snapshot as ``check_staging.py`` and run by the consumer's
CI from the vendored tree alone, with no sema dependency:

    python <vendor-dir>/check_staging.py <committed seed>

Fails when the snapshot holds a staging word the seed's ``staging.allow``
list does not name, or when the copy of the seed the snapshot was built from
(``indexes/seed_request.yaml``) differs from the committed seed. Both files
the check reads inside the snapshot are written by ``sema snapshot prepare``
in a fixed shape, so the parse below is a line scan, standard library only.
"""

from __future__ import annotations

import sys
from pathlib import Path


def staging_marker(snapshot: Path) -> tuple[list[str], list[str]]:
    """(staging words held, words the seed allowed) from
    ``indexes/staging.yaml``; both empty when the snapshot holds no staging."""
    marker = snapshot / "indexes" / "staging.yaml"
    if not marker.exists():
        return [], []
    held: list[str] = []
    allowed: list[str] = []
    current: list[str] | None = None
    for raw in marker.read_text().splitlines():
        line = raw.rstrip()
        if line.startswith("staging_words:"):
            current = held
        elif line.startswith("staging_allow:"):
            current = allowed
        elif line.startswith("- ") and current is not None:
            current.append(line[2:].strip())
        elif line and not line.startswith(" "):
            current = None
    return held, allowed


def word_name(held: str) -> str:
    """``type flo.params:004`` -> ``flo.params``."""
    return held.split(" ", 1)[1].split(":", 1)[0]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_staging.py <committed seed_request.yaml>", file=sys.stderr)
        return 2
    snapshot = Path(__file__).resolve().parent
    committed_seed = Path(argv[1]).resolve()
    vendored_seed = snapshot / "indexes" / "seed_request.yaml"

    failures: list[str] = []
    if not vendored_seed.exists():
        failures.append(f"snapshot has no {vendored_seed.relative_to(snapshot)}")
    elif vendored_seed.read_bytes() != committed_seed.read_bytes():
        failures.append(
            f"{committed_seed} differs from the seed the snapshot was built from "
            f"({vendored_seed}); regenerate the snapshot"
        )

    held, allowed = staging_marker(snapshot)
    disallowed = sorted(w for w in held if word_name(w) not in set(allowed))
    if disallowed:
        failures.append(
            "snapshot holds staging words the seed does not allow:\n  "
            + "\n  ".join(disallowed)
        )

    if failures:
        print("check_staging: FAIL", file=sys.stderr)
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    held_note = f"{len(held)} allowed staging words" if held else "published-only"
    print(f"check_staging: OK ({held_note})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
