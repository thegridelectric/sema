from pathlib import Path

import pytest
import yaml

from sema.tools.build_seed_expanded import expand_seed


def expand_request(
    tmp_path: Path, request: str, *, published_only: bool = False
) -> dict:
    request_path = tmp_path / "seed_request.yaml"
    output_path = tmp_path / "seed_expanded.yaml"
    request_path.write_text(request)
    expand_seed(request_path, output_path, published_only=published_only)
    return yaml.safe_load(output_path.read_text())


# pico.tank.module.component.gt: 000, 010, 011 published, 012 staging (the
# registry as it stands).
TANK_MODULE = """
initial_targets:
  types:
    pico.tank.module.component.gt: %s
"""


def test_published_only_bare_target_is_latest_published(tmp_path: Path) -> None:
    expanded = expand_request(tmp_path, TANK_MODULE % "{}", published_only=True)

    assert expanded["initial_targets"] == ["pico.tank.module.component.gt:011"]
    assert "012" not in expanded["worklist"]["types"]["pico.tank.module.component.gt"]


def test_published_only_include_all_passes_over_staging(tmp_path: Path) -> None:
    expanded = expand_request(
        tmp_path,
        TANK_MODULE % "\n      include_all_versions: true",
        published_only=True,
    )

    versions = set(expanded["worklist"]["types"]["pico.tank.module.component.gt"])
    assert "011" in versions
    assert "012" not in versions


def test_published_only_keeps_an_explicit_staging_version(tmp_path: Path) -> None:
    # Listed outright, a staging version is taken as written; the snapshot's
    # closure check is what refuses it.
    expanded = expand_request(
        tmp_path, TANK_MODULE % '\n      versions: ["012"]', published_only=True
    )

    assert expanded["initial_targets"] == ["pico.tank.module.component.gt:012"]


def test_structured_seed_request_uses_latest_for_empty_options(tmp_path: Path) -> None:
    expanded = expand_request(
        tmp_path,
        """
initial_targets:
  types:
    layout.lite: {}
""",
    )

    assert expanded["initial_targets"] == ["layout.lite:013"]
    assert "013" in expanded["worklist"]["types"]["layout.lite"]


def test_structured_seed_request_adds_intermediate_type_versions(
    tmp_path: Path,
) -> None:
    expanded = expand_request(
        tmp_path,
        """
initial_targets:
  types:
    layout.lite:
      versions: ["011", "013"]
""",
    )

    assert expanded["initial_targets"] == ["layout.lite:011", "layout.lite:013"]
    assert {"011", "012", "013"} <= set(expanded["worklist"]["types"]["layout.lite"])


def test_include_all_versions_uses_public_versions_only(tmp_path: Path) -> None:
    expanded = expand_request(
        tmp_path,
        """
initial_targets:
  types:
    fsm.atomic.report:
      include_all_versions: true
""",
    )

    assert expanded["initial_targets"] == [
        "fsm.atomic.report:000",
        "fsm.atomic.report:001",
    ]
    assert set(expanded["worklist"]["types"]["fsm.atomic.report"]) == {"000", "001"}
    assert "002" not in expanded["worklist"]["types"]["fsm.atomic.report"]


def test_structured_seed_request_accepts_enum_versions(tmp_path: Path) -> None:
    expanded = expand_request(
        tmp_path,
        """
initial_targets:
  enums:
    relay.energization.state:
      versions: ["000"]
""",
    )

    assert expanded["initial_targets"] == ["relay.energization.state:000"]
    assert "000" in expanded["worklist"]["enums"]["relay.energization.state"]


def test_structured_seed_request_rejects_formats_section(tmp_path: Path) -> None:
    request_path = tmp_path / "seed_request.yaml"
    output_path = tmp_path / "seed_expanded.yaml"
    request_path.write_text(
        """
initial_targets:
  formats:
    left.right.dot: {}
"""
    )

    with pytest.raises(ValueError, match="types and enums"):
        expand_seed(request_path, output_path)
