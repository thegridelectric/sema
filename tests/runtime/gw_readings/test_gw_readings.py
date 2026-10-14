import json
from pathlib import Path

from sema.runtime.codec import default_codec
from sema.runtime.types.gw_readings import GwReadings
from tests.runtime.refusal import assert_refused, axioms, mutated

# The word declares no example; its positive fixture is the mutation base.
BASE = json.loads(
    (Path(__file__).parent / "fixtures" / "v000" / "default.json").read_text()
)


def test_gw_readings_latest_version_is_000() -> None:
    assert GwReadings.version_value() == "000"


def test_default_v000_loads_as_gw_readings() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v000" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, GwReadings)
    assert decoded.type_name == "gw.readings"
    assert decoded.version == "000"
    assert decoded.channels[0].name == "vdc-relay"
    assert decoded.channel_readings_list[0].channel_name == "vdc-relay"


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.readings", "000") == {1: [], 2: []}


def test_axiom_1_refuses_window_end_not_after_start() -> None:
    def mutate(p: dict) -> None:
        p["EndUnixMs"] = p["StartUnixMs"]

    assert_refused(default_codec, mutated(BASE, mutate), 1)


def test_axiom_2_refuses_readings_without_matching_channel() -> None:
    def mutate(p: dict) -> None:
        p["ChannelReadingsList"][0]["ChannelName"] = "hp-lwt"

    assert_refused(default_codec, mutated(BASE, mutate), 2)
