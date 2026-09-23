"""Rejecting tests for gw.house0.layout/000's axioms.

The vanilla fixture is a generated House0 pair that the word accepts. Each test
mutates a copy of it so that exactly one axiom fires, and asserts the word
refuses it.
"""

import json
from pathlib import Path
from typing import Any, Callable

import pytest

from sema.runtime.types.gw_house0_layout import GwHouse0Layout

FIXTURE = Path(__file__).parent / "fixtures" / "vanilla.json"


@pytest.fixture(scope="module")
def vanilla() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text())


def mutated(
    vanilla: dict[str, Any], mutate: Callable[[dict[str, Any]], None]
) -> dict[str, Any]:
    d = json.loads(json.dumps(vanilla))
    mutate(d)
    return d


def reject(
    vanilla: dict[str, Any], mutate: Callable[[dict[str, Any]], None], axiom: str
) -> None:
    with pytest.raises(ValueError, match=axiom):
        GwHouse0Layout.model_validate(mutated(vanilla, mutate))


def drop_channel(name: str) -> Callable[[dict[str, Any]], None]:
    """Drop a channel, and drop it from the transactive-power input set with it —
    otherwise TransactivePowerChannel fires first on a metered name."""

    def mutate(d: dict[str, Any]) -> None:
        d["DataChannels"] = [c for c in d["DataChannels"] if c["Name"] != name]
        d["DerivedChannels"] = [c for c in d["DerivedChannels"] if c["Name"] != name]
        for c in d["DerivedChannels"]:
            if c["Strategy"] == "transactive-power":
                c["InputChannelNames"] = [
                    n for n in c["InputChannelNames"] if n != name
                ]

    return mutate


def test_vanilla_fixture_is_a_gw_house0_layout(vanilla: dict[str, Any]) -> None:
    layout = GwHouse0Layout.model_validate(vanilla)
    assert layout.type_name == "gw.house0.layout"
    assert layout.version == "000"


@pytest.mark.parametrize(
    "name",
    [
        "hp-odu-pwr",
        "hp-idu-pwr",
        "primary-pump-pwr",
        "store-pump-pwr",
        "dist-pump-pwr",
        "hp-lwt",
        "hp-ewt",
        "dist-swt",
        "dist-rwt",
        "store-hot-pipe",
        "store-cold-pipe",
        "buffer-hot-pipe",
        "dist-flow",
        "store-flow",
    ],
)
def test_axiom_7_required_sensing(vanilla: dict[str, Any], name: str) -> None:
    """Every name RequiredSensing lists is required in either channel collection."""
    reject(vanilla, drop_channel(name), "Axiom 7")


@pytest.mark.parametrize(
    "name",
    ["sieg-cold", "sieg-hot", "sieg-flow", "sieg-send-flow", "hp-loop-on-off-relay"],
)
def test_axiom_8_sieg_manifold_channels(vanilla: dict[str, Any], name: str) -> None:
    """The siegenthaler surface is unconditional: dropping any of it fails."""
    reject(vanilla, drop_channel(name), "Axiom 8")


def test_axiom_17_buffer_tank(vanilla: dict[str, Any]) -> None:
    """A missing buffer depth reading fails."""
    reject(vanilla, drop_channel("buffer-depth2"), "Axiom 17")


def test_axiom_17_buffer_node_name_is_not_required(vanilla: dict[str, Any]) -> None:
    """The word requires the three depth readings; the node carrying them may be
    named anything, so renaming it and its channel bindings is accepted."""

    def mutate(d: dict[str, Any]) -> None:
        for n in d["ShNodes"]:
            if n["Name"] == "buffer":
                n["Name"] = "buffer-tank"
                for key in ("ActorHierarchyName", "Handle"):
                    if n.get(key, "").endswith("buffer"):
                        n[key] = n[key][: -len("buffer")] + "buffer-tank"
        for c in d["DataChannels"]:
            if c["AboutNodeName"] == "buffer":
                c["AboutNodeName"] = "buffer-tank"
            if c["CapturedByNodeName"] == "buffer":
                c["CapturedByNodeName"] = "buffer-tank"
        for c in d["DerivedChannels"]:
            if c["CreatedByNodeName"] == "buffer":
                c["CreatedByNodeName"] = "buffer-tank"

    GwHouse0Layout.model_validate(mutated(vanilla, mutate))


def test_axiom_24_store_tank_temps(vanilla: dict[str, Any]) -> None:
    """A store tank the layout counts must carry its three depth readings."""
    reject(vanilla, drop_channel("tank2-depth3"), "Axiom 24")


def test_axiom_24_store_tank_temps_counts_every_tank(vanilla: dict[str, Any]) -> None:
    """Raising TotalStoreTanks demands the new tank's readings."""

    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["TotalStoreTanks"] += 1

    reject(vanilla, mutate, "Axiom 24")


def test_axiom_25_web_server_node_absent(vanilla: dict[str, Any]) -> None:
    """No web-server node fails."""

    def mutate(d: dict[str, Any]) -> None:
        d["ShNodes"] = [n for n in d["ShNodes"] if n["Name"] != "web-server"]
        d["Components"] = [
            c for c in d["Components"] if c["TypeName"] != "web.server.component.gt"
        ]

    reject(vanilla, mutate, "Axiom 25")


def test_axiom_25_web_server_node_wrong_actor_class(vanilla: dict[str, Any]) -> None:
    """A web-server node with an ActorClass other than NoActor fails."""

    def mutate(d: dict[str, Any]) -> None:
        for n in d["ShNodes"]:
            if n["Name"] == "web-server":
                n["ActorClass"] = "HpBoss"
                n["ActorHierarchyName"] = "s.web-server"

    reject(vanilla, mutate, "Axiom 25")


def test_axiom_26_a_slab_circuit_without_a_floor_channel(
    vanilla: dict[str, Any],
) -> None:
    """A RadiantSlab circuit SHALL name a floor-temperature channel."""

    def mutate(d: dict[str, Any]) -> None:
        circuit = d["Hydronic"]["ZoneCallCircuits"][0]
        circuit["EmitterType"] = "RadiantSlab"
        circuit.pop("FloorTempChannelName", None)

    reject(vanilla, mutate, "Axiom 26")


def test_axiom_26_a_store_under_floor_circuit_without_a_floor_channel(
    vanilla: dict[str, Any],
) -> None:
    """A StoreUnderFloor circuit carries the same obligation."""

    def mutate(d: dict[str, Any]) -> None:
        circuit = d["Hydronic"]["ZoneCallCircuits"][0]
        circuit["EmitterType"] = "StoreUnderFloor"
        circuit.pop("FloorTempChannelName", None)

    reject(vanilla, mutate, "Axiom 26")


def test_axiom_26_b_floor_channel_does_not_resolve(vanilla: dict[str, Any]) -> None:
    """A FloorTempChannelName naming no channel fails."""

    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["ZoneCallCircuits"][0]["FloorTempChannelName"] = "no-such-channel"

    reject(vanilla, mutate, "Axiom 26")


def test_axiom_26_b_floor_channel_is_not_a_temperature(vanilla: dict[str, Any]) -> None:
    """A FloorTempChannelName naming a non-temperature channel fails."""

    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["ZoneCallCircuits"][0]["FloorTempChannelName"] = "dist-flow"

    reject(vanilla, mutate, "Axiom 26")


def test_axiom_27_disabled_node_name_must_resolve(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DisabledNodeNames"] = ["no-such-node"]

    reject(vanilla, mutate, "Axiom 27")


def test_axiom_27_disabled_channel_name_must_resolve(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DisabledChannelNames"] = ["no-such-channel"]

    reject(vanilla, mutate, "Axiom 27")


def test_axiom_28_disabled_node_must_be_a_sensor(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DisabledNodeNames"] = ["admin"]

    reject(vanilla, mutate, "Axiom 28")


def test_axiom_28_disabled_sensor_disables_every_channel_it_captures(
    vanilla: dict[str, Any],
) -> None:
    def mutate(d: dict[str, Any]) -> None:
        sensor = d["DataChannels"][0]["CapturedByNodeName"]
        d["DisabledNodeNames"] = [sensor]
        d["DisabledChannelNames"] = []

    reject(vanilla, mutate, "Axiom 28")


def test_axiom_28_disabled_sensor_with_its_channels_disabled_is_accepted(
    vanilla: dict[str, Any],
) -> None:
    d = mutated(vanilla, lambda d: None)
    sensor = d["DataChannels"][0]["CapturedByNodeName"]
    captured = [
        c["Name"] for c in d["DataChannels"] if c["CapturedByNodeName"] == sensor
    ]
    derived_on = [
        x["Name"]
        for x in d["DerivedChannels"]
        if any(n in captured for n in x.get("InputChannelNames", []))
    ]
    d["DisabledNodeNames"] = [sensor]
    d["DisabledChannelNames"] = captured + derived_on
    GwHouse0Layout.model_validate(d)


def test_axiom_29_enabled_derived_channel_has_no_disabled_input(
    vanilla: dict[str, Any],
) -> None:
    def mutate(d: dict[str, Any]) -> None:
        derived = next(x for x in d["DerivedChannels"] if x.get("InputChannelNames"))
        d["DisabledChannelNames"] = [derived["InputChannelNames"][0]]

    reject(vanilla, mutate, "Axiom 29")
