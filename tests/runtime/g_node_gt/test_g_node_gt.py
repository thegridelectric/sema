import json
from pathlib import Path

from sema.runtime.codec import default_codec
from sema.runtime.types.g_node_gt import GNodeGt
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE_005 = example("g.node.gt", "005")
EXAMPLE_006 = example("g.node.gt", "006")


def _load_fixture(name: str, version_dir: str = "v005") -> dict:
    fixture = Path(__file__).parent / "fixtures" / version_dir / name
    return json.loads(fixture.read_text())


def test_g_node_gt_latest_version_is_006() -> None:
    assert GNodeGt.version_value() == "006"


def test_default_v005_upgrades_to_g_node_gt() -> None:
    decoded = default_codec.from_dict(_load_fixture("default.json"))

    assert isinstance(decoded, GNodeGt)
    assert decoded.type_name == "g.node.gt"
    assert decoded.version == "006"


def test_default_v006_pending_locationless_loads() -> None:
    decoded = default_codec.from_dict(_load_fixture("default.json", "v006"))

    assert isinstance(decoded, GNodeGt)
    assert decoded.status.value == "Pending"
    assert decoded.position_point_id is None


def test_v005_every_axiom_has_a_mutation() -> None:
    assert axioms("g.node.gt", "005") == {
        1: ["a", "b"],
        2: [],
        3: [],
        4: [],
        5: ["a", "b"],
        6: ["a", "b"],
    }


def test_v006_every_axiom_has_a_mutation() -> None:
    assert axioms("g.node.gt", "006") == {
        1: ["a", "b"],
        2: [],
        3: [],
        4: [],
        5: ["a", "b"],
        6: ["a", "b"],
    }


def test_v005_axiom_1_a_refuses_g_node_class_unlike_physical_base_class() -> None:
    def mutate(p: dict) -> None:
        p["GNodeClass"] = "MarketMaker"

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 1, clause="a")


def test_v005_axiom_1_b_refuses_logical_with_physical_g_node_class() -> None:
    def mutate(p: dict) -> None:
        p["BaseClass"] = "Logical"

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 1, clause="b")


def test_v005_axiom_2_refuses_physical_without_position_point() -> None:
    def mutate(p: dict) -> None:
        del p["PositionPointId"]

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 2)


def test_v005_axiom_3_refuses_prev_alias_equal_to_alias() -> None:
    def mutate(p: dict) -> None:
        p["PrevAlias"] = p["Alias"]

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 3)


def test_v005_axiom_4_refuses_g_node_class_with_whitespace() -> None:
    def mutate(p: dict) -> None:
        p["BaseClass"] = "Logical"
        p["GNodeClass"] = "Scada Service"

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 4)


def test_v005_axiom_5_a_refuses_terminal_asset_without_ta_suffix() -> None:
    def mutate(p: dict) -> None:
        p["BaseClass"] = "TerminalAsset"
        p["GNodeClass"] = "TerminalAsset"

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 5, clause="a")


def test_v005_axiom_5_b_refuses_scada_without_scada_suffix() -> None:
    def mutate(p: dict) -> None:
        p["BaseClass"] = "Logical"
        p["GNodeClass"] = "Scada"

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 5, clause="b")


def test_v005_axiom_6_a_refuses_single_word_alias() -> None:
    def mutate(p: dict) -> None:
        p["Alias"] = "isone"

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 6, clause="a")


def test_v005_axiom_6_b_refuses_single_word_prev_alias() -> None:
    def mutate(p: dict) -> None:
        p["PrevAlias"] = "isone"

    assert_refused(default_codec, mutated(EXAMPLE_005, mutate), 6, clause="b")


def test_v006_axiom_2_refuses_active_physical_without_position_point() -> None:
    def mutate(p: dict) -> None:
        del p["PositionPointId"]

    assert_refused(default_codec, mutated(EXAMPLE_006, mutate), 2)
