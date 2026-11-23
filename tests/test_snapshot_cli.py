import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from sema.interfaces.cli import snapshot


ROOT = Path(__file__).resolve().parents[1]


def staging_seed(tmp_path: Path) -> tuple[Path, str]:
    """A seed naming one staging type version outright, chosen from the
    registry at test time so the test survives promotions. Returns the seed
    path and the word as the CLI prints it."""
    registry = yaml.safe_load((ROOT / "definitions" / "registry.yaml").read_text())
    for name, entry in sorted(registry["types"].items()):
        for version, version_entry in sorted((entry.get("versions") or {}).items()):
            if version_entry.get("status") == "staging":
                seed = tmp_path / "staging_seed_request.yaml"
                seed.write_text(
                    f"initial_targets:\n  types:\n    {name}:\n"
                    f'      versions: ["{version}"]\n'
                )
                return seed, f"type {name}:{version}"
    pytest.skip("no staging type version in the registry")


def staging_closure_names(word: str) -> list[str]:
    """The names of ``word`` and every staging word in its dependency
    closure: what a seed's ``staging.allow`` must list to hold it."""
    name, _, version = word.split(" ", 1)[1].partition(":")
    registry = yaml.safe_load((ROOT / "definitions" / "registry.yaml").read_text())
    closure = yaml.safe_load((ROOT / "indexes" / "dependency_closure.yaml").read_text())

    def flatten(node: object) -> set[str]:
        if isinstance(node, list):
            return set(node)
        if isinstance(node, dict):
            return set().union(*(flatten(v) for v in node.values()))
        return set()

    def status(ref: str) -> str:
        ref_name, _, ref_version = ref.partition(":")
        for section in ("types", "enums", "formats"):
            entry = registry[section].get(ref_name)
            if entry is None:
                continue
            if "versions" in entry and ref_version:
                return entry["versions"][ref_version]["status"]
            return entry["status"]
        raise KeyError(ref)

    deps = flatten(closure["types"][name][version])
    names = {name} | {d.partition(":")[0] for d in deps if status(d) == "staging"}
    return sorted(names)


def allowing_seed(tmp_path: Path, word: str, allow: list[str]) -> Path:
    """``staging_seed``'s seed with a ``staging.allow`` block."""
    name, _, version = word.split(" ", 1)[1].partition(":")
    seed = tmp_path / "allowing_seed_request.yaml"
    allow_lines = "".join(f"    - {w}\n" for w in allow)
    seed.write_text(
        f"initial_targets:\n  types:\n    {name}:\n"
        f'      versions: ["{version}"]\n'
        f"staging:\n  allow:\n{allow_lines}"
    )
    return seed


def test_snapshot_prepare_rejects_staging_by_default(
    monkeypatch, tmp_path: Path
) -> None:
    # A seed that names a staging version outright fails the published-only
    # default and names the staging offender.
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    seed, word = staging_seed(tmp_path)
    with pytest.raises(ValueError, match="STAGING") as excinfo:
        snapshot.prepare_snapshot(seed)
    assert word in str(excinfo.value)


def test_published_only_prepare_refuses_a_staging_only_seed_word(
    monkeypatch, tmp_path: Path
) -> None:
    # include_all_versions on a word with no published version must fail the
    # published-only default and name the word, rather than omit it.
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    registry = yaml.safe_load((ROOT / "indexes" / "public_registry.yaml").read_text())
    name = None
    for candidate, entry in sorted(registry["types"].items()):
        versions = entry.get("versions") or {}
        if entry.get("versioning_strategy") == "none" or not versions:
            continue
        if all(version.get("status") == "staging" for version in versions.values()):
            name = candidate
            break
    if name is None:
        pytest.skip("no staging-only versioned type in the registry")
    seed = tmp_path / "seed_request.yaml"
    seed.write_text(
        f"initial_targets:\n  types:\n    {name}:\n      include_all_versions: true\n"
    )
    with pytest.raises(ValueError, match="will not skip") as excinfo:
        snapshot.prepare_snapshot(seed)
    assert name in str(excinfo.value)
    assert not (tmp_path / "output").exists()


def test_published_only_prepare_passes_over_staging_versions(
    monkeypatch, tmp_path: Path
) -> None:
    # A seed that names no staging version outright builds published-only
    # although the word's latest version is staging: no marker, no banner.
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    seed = tmp_path / "seed_request.yaml"
    seed.write_text(
        "initial_targets:\n  types:\n    pico.tank.module.component.gt:\n"
        "      include_all_versions: true\n"
    )
    target_root = snapshot.prepare_snapshot(seed)

    expanded = (target_root / "indexes" / "seed_expanded.yaml").read_text()
    assert "pico.tank.module.component.gt:011" in expanded
    assert "pico.tank.module.component.gt:012" not in expanded
    assert not (target_root / "indexes" / "staging.yaml").exists()
    assert "PLEASE ONLY USE IN DEV" not in (target_root / "README.md").read_text()


def test_refused_prepare_leaves_previous_output_intact(
    monkeypatch, tmp_path: Path
) -> None:
    # A refusal must fire BEFORE output/ is cleared: a cleared-then-refused
    # output/ silently guts whatever a consumer mirrors next (rsync --delete).
    output_root = tmp_path / "output"
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", output_root)
    seed, word = staging_seed(tmp_path)
    allowing = allowing_seed(tmp_path, word, staging_closure_names(word))
    target_root = snapshot.prepare_snapshot(allowing)
    before = sorted(p.relative_to(target_root) for p in target_root.rglob("*"))
    assert before

    with pytest.raises(ValueError, match="STAGING"):
        snapshot.prepare_snapshot(seed)

    after = sorted(p.relative_to(target_root) for p in target_root.rglob("*"))
    assert after == before


def test_seed_allow_writes_the_dev_only_markers(monkeypatch, tmp_path: Path) -> None:
    # A seed whose staging.allow names the closure's staging words builds,
    # with the dev-only markers: indexes/staging.yaml listing the words held
    # and the words allowed, and the README banner naming the word.
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    _, word = staging_seed(tmp_path)
    allow = staging_closure_names(word)
    target_root = snapshot.prepare_snapshot(allowing_seed(tmp_path, word, allow))
    marker = yaml.safe_load((target_root / "indexes" / "staging.yaml").read_text())
    assert marker["staging"] is True
    assert word in marker["staging_words"]
    assert marker["staging_allow"] == allow
    readme = (target_root / "README.md").read_text()
    assert "PLEASE ONLY USE IN DEV" in readme
    assert word in readme
    assert (target_root / "check_staging.py").exists()


def test_seed_allow_must_cover_the_closure(monkeypatch, tmp_path: Path) -> None:
    # Allowing the root alone is not enough when its closure reaches another
    # staging word: the refusal names that word, not the root.
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    _, word = staging_seed(tmp_path)
    name = word.split(" ", 1)[1].partition(":")[0]
    allow = staging_closure_names(word)
    if allow == [name]:
        pytest.skip("the staging word's closure reaches no other staging word")
    with pytest.raises(ValueError, match="does not allow") as excinfo:
        snapshot.prepare_snapshot(allowing_seed(tmp_path, word, [name]))
    message = str(excinfo.value)
    assert word not in message
    assert any(other in message for other in allow if other != name)
    assert not (tmp_path / "output").exists()


def test_seed_allow_names_words_not_versions(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    _, word = staging_seed(tmp_path)
    versioned = word.split(" ", 1)[1]
    with pytest.raises(ValueError, match="names words, not versions"):
        snapshot.prepare_snapshot(allowing_seed(tmp_path, word, [versioned]))


def test_published_only_prepare_reports_passed_over_versions(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    seed = tmp_path / "seed_request.yaml"
    seed.write_text(
        "initial_targets:\n  types:\n    pico.tank.module.component.gt:\n"
        "      include_all_versions: true\n"
    )
    snapshot.prepare_snapshot(seed)
    out = capsys.readouterr().out
    assert "passed over staging version pico.tank.module.component.gt:012" in out


def run_check(snapshot_root: Path, committed_seed: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            "-I",
            str(snapshot_root / "check_staging.py"),
            str(committed_seed),
        ],
        capture_output=True,
        text=True,
    )


def test_shipped_check_passes_a_snapshot_its_seed_allows(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    _, word = staging_seed(tmp_path)
    seed = allowing_seed(tmp_path, word, staging_closure_names(word))
    target_root = snapshot.prepare_snapshot(seed)
    result = run_check(target_root, seed)
    assert result.returncode == 0, result.stderr
    assert "allowed staging words" in result.stdout


def test_shipped_check_fails_when_the_committed_seed_changed(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    _, word = staging_seed(tmp_path)
    seed = allowing_seed(tmp_path, word, staging_closure_names(word))
    target_root = snapshot.prepare_snapshot(seed)
    seed.write_text(seed.read_text() + "# edited after the build\n")
    result = run_check(target_root, seed)
    assert result.returncode == 1
    assert "differs from the seed the snapshot was built from" in result.stderr


def test_shipped_check_fails_on_staging_the_seed_does_not_allow(
    monkeypatch, tmp_path: Path
) -> None:
    # The vendored marker and the vendored seed disagree only when a snapshot
    # was built some other way than prepare; the check still catches it.
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", tmp_path / "output")
    _, word = staging_seed(tmp_path)
    seed = allowing_seed(tmp_path, word, staging_closure_names(word))
    target_root = snapshot.prepare_snapshot(seed)
    marker = target_root / "indexes" / "staging.yaml"
    marker.write_text(
        marker.read_text().replace("staging_allow:", "staging_allow: []\nx_:")
    )
    result = run_check(target_root, seed)
    assert result.returncode == 1
    assert "does not allow" in result.stderr
    assert word in result.stderr


def test_snapshot_prepare_and_build_write_sema_at_output_root(
    monkeypatch, tmp_path: Path
) -> None:
    output_root = tmp_path / "output"
    monkeypatch.setattr(snapshot, "OUTPUT_DIR", output_root)

    target_root = snapshot.prepare_snapshot(ROOT / "template_seed_request.yaml")

    assert target_root == output_root / "sema"
    assert not (output_root / "gjk").exists()
    assert not (output_root / "seed_expanded.yaml").exists()
    assert (target_root / "indexes" / "seed_expanded.yaml").exists()
    assert (target_root / "indexes" / "local_names.yaml").exists()
    assert not (target_root / "base.py").exists()
    # The template seed's closure is published, so no dev-only markers.
    assert not (target_root / "indexes" / "staging.yaml").exists()
    assert "PLEASE ONLY USE IN DEV" not in (target_root / "README.md").read_text()

    stale_file = output_root / "stale.txt"
    stale_file.write_text("remove me")
    local_names = target_root / "indexes" / "local_names.yaml"
    local_names.write_text(
        local_names.read_text().replace(
            "layout.lite: layout.lite", "layout.lite: lite.layout"
        )
    )

    assert snapshot.prepare_snapshot(ROOT / "template_seed_request.yaml") == target_root
    assert not stale_file.exists()
    assert "lite.layout" not in local_names.read_text()
    local_names.write_text(
        local_names.read_text()
        .replace("layout.lite: layout.lite", "layout.lite: lite.layout")
        .replace(
            "gw1.emission.method: gw1.emission.method",
            "gw1.emission.method: emission.method",
        )
        .replace(
            "gw1.seasonal.storage.mode: gw1.seasonal.storage.mode",
            "gw1.seasonal.storage.mode: seasonal.storage.mode",
        )
    )

    assert snapshot.build_snapshot_runtime("gjk") == target_root
    assert (target_root / "base.py").exists()
    assert (target_root / "codec.py").exists()
    assert (target_root / "property_format.py").exists()
    assert (target_root / "definitions" / "registry.yaml").exists()
    assert (target_root / "indexes" / "dependency_closure.yaml").exists()
    assert (target_root / "indexes" / "lookup.yaml").exists()
    assert (target_root / "indexes" / "reverse_dependencies.yaml").exists()
    assert (target_root / "indexes" / "versions.yaml").exists()
    # Snapshots ship data, not test code: no vendored tests/ directory.
    assert not (target_root / "tests").exists()
    # Round-trip harness + generated samples ship instead.
    assert (target_root / "roundtrip.py").exists()
    assert (target_root / "samples" / "README.md").exists()
    sample_files = list((target_root / "samples").glob("*.json"))
    assert sample_files, "expected at least one generated sample"
    assert any("channel.readings.list.item" in p.name for p in sample_files)
    assert "from gjk.sema.base import" in (target_root / "codec.py").read_text()
    assert (target_root / "enums" / "emission_method.py").exists()
    assert not (target_root / "enums" / "gw1_emission_method.py").exists()
    enum_init = (target_root / "enums" / "__init__.py").read_text()
    lite_layout = (target_root / "types" / "lite_layout.py").read_text()
    assert "class LiteLayout" in lite_layout
    assert "from gjk.sema.logic" not in lite_layout
    assert "def check_axiom_1" in lite_layout
    assert (
        "from gjk.sema.enums.seasonal_storage_mode import SeasonalStorageMode"
        in enum_init
    )
    # layout.lite 013 references no enum directly; 012 still does, and the
    # vendored old version must import it through the package.
    lite_layout_012 = (
        target_root / "types" / "old_versions" / "lite_layout_012.py"
    ).read_text()
    assert "from gjk.sema.enums import SeasonalStorageMode" in lite_layout_012

    assert snapshot.build_snapshot_runtime("gjk") == target_root
    assert "def check_axiom_1" in (target_root / "types" / "lite_layout.py").read_text()
    assert (
        "def upgrade"
        in (target_root / "types" / "old_versions" / "lite_layout_011.py").read_text()
    )
