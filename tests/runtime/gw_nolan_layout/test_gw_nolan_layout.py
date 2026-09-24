"""Rejecting tests for gw.nolan.layout/000's axioms.

The vanilla fixture is a generated Nolan pair that the word accepts. Each test
mutates a copy of it so that exactly one axiom fires, and asserts the word
refuses it.
"""

import json
from pathlib import Path
from typing import Any, Callable

import pytest

from sema.runtime.types.gw_nolan_layout import GwNolanLayout

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
        GwNolanLayout.model_validate(mutated(vanilla, mutate))


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


def drop_node(name: str) -> Callable[[dict[str, Any]], None]:
    def mutate(d: dict[str, Any]) -> None:
        d["ShNodes"] = [n for n in d["ShNodes"] if n["Name"] != name]

    return mutate


def test_vanilla_fixture_is_a_gw_nolan_layout(vanilla: dict[str, Any]) -> None:
    layout = GwNolanLayout.model_validate(vanilla)
    assert layout.type_name == "gw.nolan.layout"
    assert layout.version == "000"


@pytest.mark.parametrize("name", ["backup", "scada-blind"])
def test_axiom_4_command_nodes_state_anchors(
    vanilla: dict[str, Any], name: str
) -> None:
    """backup and scada-blind are command nodes in every Nolan layout."""
    reject(vanilla, drop_node(name), "Axiom 4")


def test_axiom_5_vdc_relay_is_required(vanilla: dict[str, Any]) -> None:
    reject(vanilla, drop_node("vdc-relay"), "Axiom 5")


@pytest.mark.parametrize(
    "name",
    [
        "hp-lwt",
        "hp-ewt",
        "dist-swt",
        "dist-rwt",
        "store-hot-pipe",
        "store-cold-pipe",
        "secondary-lwt",
        "secondary-ewt",
        "buffer-cold-pipe",
        "fancoil-swt",
        "fancoil-rwt",
        "floor-swt",
        "floor-rwt",
        "dist-flow",
        "primary-flow",
        "store-flow",
        "secondary-flow",
        "hp-odu-pwr",
        "hp-ctrl-box-pwr",
        "primary-pump-pwr",
        "store-pump-pwr",
        "dist-pump-pwr",
        "secondary-pump-pwr",
        "buffer-top-elt-pwr",
        "tank1-bottom-elt-pwr",
    ],
)
def test_axiom_8_required_sensing(vanilla: dict[str, Any], name: str) -> None:
    """Every name RequiredSensing lists is required in either channel collection."""
    reject(vanilla, drop_channel(name), "Axiom 8")


@pytest.mark.parametrize("name", ["buffer-depth1-device", "tank1-depth3-device"])
def test_axiom_8_device_names_are_not_required(
    vanilla: dict[str, Any], name: str
) -> None:
    """The word requires the depth readings; the raw channel a home derives one
    from may be spelled anything, so renaming it is accepted."""

    def mutate(d: dict[str, Any]) -> None:
        renamed = name.replace("-device", "-raw")
        for c in d["DataChannels"]:
            if c["Name"] == name:
                c["Name"] = renamed
        for c in d["DerivedChannels"]:
            c["InputChannelNames"] = [
                renamed if n == name else n for n in c["InputChannelNames"]
            ]

    GwNolanLayout.model_validate(mutated(vanilla, mutate))


def test_axiom_20_buffer_tank(vanilla: dict[str, Any]) -> None:
    """A missing buffer depth reading fails."""
    reject(vanilla, drop_channel("buffer-depth2"), "Axiom 20")


def test_axiom_21_store_tank_temps(vanilla: dict[str, Any]) -> None:
    """The store tank must carry its three depth readings."""
    reject(vanilla, drop_channel("tank1-depth3"), "Axiom 21")


@pytest.mark.parametrize("name", ["usable-energy", "required-energy"])
def test_axiom_22_system_model_energy_channels_absent(
    vanilla: dict[str, Any], name: str
) -> None:
    """Both system-model energy channels are required."""
    reject(vanilla, drop_channel(name), "Axiom 22")


def test_axiom_22_system_model_energy_channels_wrong_strategy(
    vanilla: dict[str, Any],
) -> None:
    """A usable-energy channel on another strategy fails."""

    def mutate(d: dict[str, Any]) -> None:
        for c in d["DerivedChannels"]:
            if c["Name"] == "usable-energy":
                c["Strategy"] = "identity"

    reject(vanilla, mutate, "Axiom 22")


def test_axiom_22_system_model_energy_channels_same_model_twice(
    vanilla: dict[str, Any],
) -> None:
    """The two channels name one model each, never the same model twice."""

    def mutate(d: dict[str, Any]) -> None:
        for c in d["DerivedChannels"]:
            if c["Name"] == "required-energy":
                c["Parameters"]["EnergyModel"]["TypeName"] = "gw0.usable.energy.layered"

    reject(vanilla, mutate, "Axiom 22")


def test_axiom_23_web_server_node_absent(vanilla: dict[str, Any]) -> None:
    """No web-server node fails."""

    def mutate(d: dict[str, Any]) -> None:
        d["ShNodes"] = [n for n in d["ShNodes"] if n["Name"] != "web-server"]
        d["Components"] = [
            c for c in d["Components"] if c["TypeName"] != "web.server.component.gt"
        ]

    reject(vanilla, mutate, "Axiom 23")


def test_axiom_23_web_server_node_wrong_actor_class(vanilla: dict[str, Any]) -> None:
    """A web-server node with an ActorClass other than NoActor fails."""

    def mutate(d: dict[str, Any]) -> None:
        for n in d["ShNodes"]:
            if n["Name"] == "web-server":
                n["ActorClass"] = "HpBoss"
                n["ActorHierarchyName"] = "s.web-server"

    reject(vanilla, mutate, "Axiom 23")


def test_axiom_24_a_slab_circuit_without_a_floor_channel(
    vanilla: dict[str, Any],
) -> None:
    """A RadiantSlab circuit SHALL name a floor-temperature channel."""

    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["ZoneCallCircuits"][0].pop("FloorTempChannelName", None)

    reject(vanilla, mutate, "Axiom 24")


def test_axiom_24_b_floor_channel_does_not_resolve(vanilla: dict[str, Any]) -> None:
    """A FloorTempChannelName naming no channel fails."""

    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["ZoneCallCircuits"][0]["FloorTempChannelName"] = "no-such-channel"

    reject(vanilla, mutate, "Axiom 24")


def test_axiom_24_b_floor_channel_is_not_a_temperature(vanilla: dict[str, Any]) -> None:
    """A FloorTempChannelName naming a non-temperature channel fails."""

    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["ZoneCallCircuits"][0]["FloorTempChannelName"] = "dist-flow"

    reject(vanilla, mutate, "Axiom 24")


def test_axiom_24_fan_coil_circuit_needs_no_floor_channel(
    vanilla: dict[str, Any],
) -> None:
    """A FanCoil circuit carries no floor-temperature obligation."""
    GwNolanLayout.model_validate(vanilla)
    assert not any(
        "FloorTempChannelName" in c
        for c in vanilla["Hydronic"]["ZoneCallCircuits"]
        if c["EmitterType"] == "FanCoil"
    )


def test_axiom_25_disabled_node_name_must_resolve(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DisabledNodeNames"] = ["no-such-node"]

    reject(vanilla, mutate, "Axiom 25")


def test_axiom_25_disabled_channel_name_must_resolve(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DisabledChannelNames"] = ["no-such-channel"]

    reject(vanilla, mutate, "Axiom 25")


def test_axiom_26_disabled_node_must_be_a_sensor(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DisabledNodeNames"] = ["admin"]

    reject(vanilla, mutate, "Axiom 26")


def test_axiom_26_disabled_sensor_disables_every_channel_it_captures(
    vanilla: dict[str, Any],
) -> None:
    def mutate(d: dict[str, Any]) -> None:
        sensor = d["DataChannels"][0]["CapturedByNodeName"]
        d["DisabledNodeNames"] = [sensor]
        d["DisabledChannelNames"] = []

    reject(vanilla, mutate, "Axiom 26")


def test_axiom_26_disabled_sensor_with_its_channels_disabled_is_accepted(
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
    GwNolanLayout.model_validate(d)


def test_axiom_27_enabled_derived_channel_has_no_disabled_input(
    vanilla: dict[str, Any],
) -> None:
    def mutate(d: dict[str, Any]) -> None:
        derived = next(x for x in d["DerivedChannels"] if x.get("InputChannelNames"))
        d["DisabledChannelNames"] = [derived["InputChannelNames"][0]]

    reject(vanilla, mutate, "Axiom 27")


def test_axiom_28_a_actuator_without_a_channel(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["DataChannels"] = [c for c in d["DataChannels"] if c["Name"] != "vdc-relay"]

    reject(vanilla, mutate, "Axiom 28")


def test_axiom_28_a_actuator_channel_about_another_node(
    vanilla: dict[str, Any],
) -> None:
    def mutate(d: dict[str, Any]) -> None:
        channel = next(c for c in d["DataChannels"] if c["Name"] == "vdc-relay")
        channel["AboutNodeName"] = "hp-scada-ops-relay"

    reject(vanilla, mutate, "Axiom 28")


def test_axiom_28_a_circuit_relay_without_a_channel(vanilla: dict[str, Any]) -> None:
    def mutate(d: dict[str, Any]) -> None:
        relay = d["Hydronic"]["ZoneCallCircuits"][0]["OpsRelayNode"]
        d["DataChannels"] = [c for c in d["DataChannels"] if c["Name"] != relay]

    reject(vanilla, mutate, "Axiom 28")


@pytest.mark.parametrize(
    ("name", "telemetry", "quantity"),
    [
        ("vdc-relay", "VoltsTimesTen", "Voltage"),
        ("secondary-010v", "RelayState", "Unitless"),
    ],
)
def test_axiom_28_b_actuator_channel_telemetry(
    vanilla: dict[str, Any], name: str, telemetry: str, quantity: str
) -> None:
    """A relay channel carrying a voltage, or an output channel carrying a relay
    state, is refused; the quantity moves with the telemetry so data.channel.gt's
    own consistency axiom is not what fires."""

    def mutate(d: dict[str, Any]) -> None:
        channel = next(c for c in d["DataChannels"] if c["Name"] == name)
        channel["TelemetryName"] = telemetry
        channel["Quantity"] = quantity

    reject(vanilla, mutate, "Axiom 28")


def test_axiom_29_scada_control_against_the_control_box_factory_pump(
    vanilla: dict[str, Any],
) -> None:
    """Spruce's Samsung control box ships its pump with no override, so declaring
    Scada control of the primary pump is refused."""

    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["PrimaryPumpOwner"] = "Scada"

    reject(vanilla, mutate, "Axiom 29")


def test_axiom_29_scada_control_with_an_overridable_control_box_is_accepted(
    vanilla: dict[str, Any],
) -> None:
    def mutate(d: dict[str, Any]) -> None:
        d["Hydronic"]["PrimaryPumpOwner"] = "Scada"
        box = next(
            r
            for r in d["DeviceTypes"]
            if r["TypeName"] == "hp.control.box.device.type.gt"
        )
        box["PrimaryPumpOverridable"] = True

    GwNolanLayout.model_validate(mutated(vanilla, mutate))
