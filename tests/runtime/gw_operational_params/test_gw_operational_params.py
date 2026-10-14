import json
from pathlib import Path

from sema.runtime.codec import default_codec
from sema.runtime.types.gw_operational_params import GwOperationalParams
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("gw.operational.params", "000")


def test_default_v000_loads_as_gw_operational_params() -> None:
    fixture = Path(__file__).parent / "fixtures" / "v000" / "default.json"
    payload = json.loads(fixture.read_text())

    decoded = default_codec.from_dict(payload)

    assert isinstance(decoded, GwOperationalParams)
    assert decoded.type_name == "gw.operational.params"
    assert decoded.version == "000"
    assert decoded.standby is False


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("gw.operational.params", "000") == {1: [], 2: [], 3: [], 4: [], 5: []}


def test_axiom_5_refuses_standby_house0_loop_not_at_full_send() -> None:
    def mutate(p: dict) -> None:
        p["Standby"] = True
        p["DispatchHold"]["OperatorHold"] = True

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 5)
