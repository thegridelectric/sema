"""gw1.scada.device.type.gt axioms, proved by mutation of the word's example."""

from sema.runtime.codec import default_codec
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw1.scada.device.type.gt", "000")

DAC_MUX = {
    "MuxName": "DacMux",
    "I2cBus": "DefaultBus",
    "I2cAddress": 112,
    "MuxType": "Tca9548a",
    "Channels": 8,
    "TypeName": "i2c.mux",
    "Version": "000",
}

ZONES_DAC = {
    "DacName": "Zones456",
    "I2cBus": "DefaultBus",
    "I2cAddress": 96,
    "MuxName": "DacMux",
    "MuxChannel": 2,
    "DacType": "Mcp4728",
    "Channels": 4,
    "TypeName": "i2c.dac.capability",
    "Version": "000",
}


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw1.scada.device.type.gt", "000") == {
        1: [],
        2: [],
        3: [],
        4: ["a", "b", "c"],
        5: [],
        6: [],
    }


def test_axiom_1_refuses_bus_not_in_bus_list() -> None:
    def mutate(p: dict) -> None:
        p["Expanders"][0]["I2cBus"] = "GhostBus"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_expander_not_in_expanders() -> None:
    def mutate(p: dict) -> None:
        p["I2cRelays"][1]["ExpanderIdx"] = 3

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_axiom_4_a_refuses_mux_not_in_muxes() -> None:
    def mutate(p: dict) -> None:
        p["Dacs"] = [{**ZONES_DAC, "MuxName": "GhostMux"}]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, clause="a")


def test_axiom_4_b_refuses_mux_channel_out_of_bounds() -> None:
    def mutate(p: dict) -> None:
        p["Muxes"] = [DAC_MUX]
        p["Dacs"] = [{**ZONES_DAC, "MuxChannel": 9}]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, clause="b")


def test_axiom_4_c_refuses_dac_bus_unlike_mux_bus() -> None:
    def mutate(p: dict) -> None:
        p["BusList"].append(
            {
                "Name": "SecondBus",
                "BusNumber": 2,
                "TypeName": "i2c.bus",
                "Version": "000",
            }
        )
        p["Muxes"] = [DAC_MUX]
        p["Dacs"] = [{**ZONES_DAC, "I2cBus": "SecondBus"}]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4, clause="c")


def test_axiom_5_refuses_energized_level_out_of_range() -> None:
    def mutate(p: dict) -> None:
        p["RelayEnergizedLevel"] = 2

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 5)


def test_axiom_6_refuses_two_buses() -> None:
    def mutate(p: dict) -> None:
        p["BusList"].append(
            {
                "Name": "SecondBus",
                "BusNumber": 3,
                "TypeName": "i2c.bus",
                "Version": "000",
            }
        )

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 6)
