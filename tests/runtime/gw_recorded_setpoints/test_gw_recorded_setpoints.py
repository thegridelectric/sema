import json
from pathlib import Path

from sema.runtime.codec import default_codec
from sema.runtime.types.gw_recorded_setpoints import GwRecordedSetpoints
from tests.runtime.refusal import assert_refused, axioms, mutated

# The word declares no example; its positive fixture is the mutation base.
BASE = json.loads(
    (Path(__file__).parent / "fixtures" / "v000" / "default.json").read_text()
)


def test_default_v000_loads_as_gw_recorded_setpoints() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v000" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, GwRecordedSetpoints)
    assert decoded.type_name == "gw.recorded.setpoints"
    assert decoded.version == "000"
    assert decoded.setpoint_list[0].channel_name == "zone1-bedrooms-set"


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.recorded.setpoints", "000") == {1: []}


def test_axiom_1_refuses_a_channel_recorded_twice() -> None:
    def mutate(p: dict) -> None:
        p["SetpointList"][1]["ChannelName"] = p["SetpointList"][0]["ChannelName"]

    assert_refused(default_codec, mutated(BASE, mutate), 1)
