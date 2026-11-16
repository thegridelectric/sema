"""Constant types: a type marked `x-gridworks.constant: true` has every
property `const` and required, no additional properties, exactly one
version `000`, and no `$ref`, union, inline object or axiom (spec
authoring/types.md "Constant Types", registry/types.md "Constant Types").
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFINITIONS = ROOT / "definitions"
REGISTRY = DEFINITIONS / "registry.yaml"

SCALAR = (str, int, float, bool, type(None))


def constant_types() -> dict[str, dict]:
    """type name -> registry entry for every constant type."""
    registry = yaml.safe_load(REGISTRY.read_text())
    out = {}
    for name, entry in registry["types"].items():
        versions = entry.get("versions") or {}
        for version in versions:
            schema = yaml.safe_load(
                (DEFINITIONS / "types" / name / f"{version}.yaml").read_text()
            )
            if schema.get("x-gridworks", {}).get("constant") is True:
                out[name] = entry
    return out


def test_a_constant_has_exactly_version_000() -> None:
    for name, entry in constant_types().items():
        assert list(entry["versions"]) == ["000"], (
            f"{name}: a constant has exactly one version, 000; a changed value "
            f"is a new constant with a new name"
        )
        assert entry["versioning_strategy"] == "literal", name
        assert entry["latest_version"] == "000", name


def test_every_instance_of_a_constant_is_the_same_json() -> None:
    for name in constant_types():
        schema = yaml.safe_load((DEFINITIONS / "types" / name / "000.yaml").read_text())
        props = schema["properties"]
        assert schema.get("additionalProperties") is False, name
        assert sorted(schema["required"]) == sorted(props), (
            f"{name}: every property of a constant is required"
        )
        for prop, defn in props.items():
            assert set(defn) <= {"const", "description"}, (
                f"{name}.{prop}: a constant property has only const and description, "
                f"got {sorted(defn)}"
            )
            assert "const" in defn, f"{name}.{prop}: a constant property is const"
            assert isinstance(defn["const"], SCALAR), (
                f"{name}.{prop}: a const value is a JSON scalar"
            )
        assert "axioms" not in schema["x-gridworks"], name
        assert schema["x-gridworks"].get("constant") is True, name
        keys = list(schema["x-gridworks"])
        assert keys[:2] == ["owner", "constant"], (
            f"{name}: constant comes directly after owner in x-gridworks, got {keys}"
        )


def test_there_is_at_least_one_constant() -> None:
    assert "dispatch.terms.first.isone.hack" in constant_types()
