"""scada.control.capabilities axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("scada.control.capabilities", "001")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("scada.control.capabilities", "001") == {
        1: ["a", "b", "c"],
        2: [],
        3: [],
        4: ["a", "b"],
    }


def test_axiom_1_c_refuses_relay_class_in_command_nodes() -> None:
    def mutate(p: dict) -> None:
        p["CommandNodes"][0]["ActorClass"] = "Relay"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1, clause="c")


def test_axiom_2_refuses_command_node_handle_terminal_mismatch() -> None:
    def mutate(p: dict) -> None:
        p["CommandNodes"][0]["Handle"] = "admin.cycler"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_4_a_refuses_directly_commanded_node_without_interface() -> None:
    def mutate(p: dict) -> None:
        p["CommandInterfaces"] = [
            i for i in p["CommandInterfaces"] if i["ActorName"] != "hp-boss"
        ]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, clause="a")


def test_axiom_4_b_refuses_duplicate_interface_actor_name() -> None:
    def mutate(p: dict) -> None:
        p["CommandInterfaces"].append(p["CommandInterfaces"][0])

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, clause="b")


EXAMPLE_003 = example("scada.control.capabilities", "003")


def test_003_every_axiom_has_a_mutation() -> None:
    assert axioms("scada.control.capabilities", "003") == {
        1: ["a", "b", "c"],
        2: [],
        3: [],
        4: ["a", "b", "c"],
    }


def test_003_axiom_4_a_refuses_directly_commanded_node_without_interface() -> None:
    def mutate(p: dict) -> None:
        p["CommandInterfaces"] = [
            i for i in p["CommandInterfaces"] if i["ActorName"] != "hp-boss"
        ]

    assert_refused(default_codec, mutated(EXAMPLE_003, mutate), 4, clause="a")


def test_003_axiom_4_a_refuses_owned_relay_interface_admin_may_not_take() -> None:
    """An owned relay is in the cover only through AdminMayTake."""

    def mutate(p: dict) -> None:
        for i in p["CommandInterfaces"]:
            if i["ActorName"] == "secondary-pump-relay":
                i["AdminMayTake"] = False

    assert_refused(default_codec, mutated(EXAMPLE_003, mutate), 4, clause="a")


def test_003_axiom_4_b_refuses_duplicate_interface_actor_name() -> None:
    def mutate(p: dict) -> None:
        p["CommandInterfaces"].append(p["CommandInterfaces"][0])

    assert_refused(default_codec, mutated(EXAMPLE_003, mutate), 4, clause="b")


def test_003_axiom_4_c_refuses_admin_may_take_on_a_command_node() -> None:
    def mutate(p: dict) -> None:
        for i in p["CommandInterfaces"]:
            if i["ActorName"] == "hp-boss":
                i["AdminMayTake"] = True

    assert_refused(default_codec, mutated(EXAMPLE_003, mutate), 4, clause="c")
