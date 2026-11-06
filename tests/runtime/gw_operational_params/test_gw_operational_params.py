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
    assert axioms("gw.operational.params", "000") == {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: ["a"],
    }


def test_axiom_5_refuses_standby_house0_loop_not_at_full_send() -> None:
    def mutate(p: dict) -> None:
        p["Standby"] = True
        p["DispatchHold"]["OperatorHold"] = True

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 5)


def no_sieg_family(p: dict) -> None:
    p["FamilyParams"] = {
        "KeepBufferFull": False,
        "SeasonalStorageMode": "AllTanks",
        "TypeName": "gw.house0.no.sieg.family.params",
        "Version": "000",
    }


def test_the_no_sieg_family_is_a_family() -> None:
    default_codec.from_dict(mutated(EXAMPLE, no_sieg_family))


def test_axiom_4_d_refuses_no_sieg_no_heating_without_its_relays() -> None:
    def mutate(p: dict) -> None:
        no_sieg_family(p)
        p["StandbyPosture"] = "NoHeatingOrCooling"
        p["EnergizedStandbyRelays"] = []

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 4)


def test_axiom_6_refuses_alice_without_operator_hold() -> None:
    def mutate(p: dict) -> None:
        p["DispatchHold"]["OperatorHold"] = False

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 6)


def test_bruce_runs_without_operator_hold() -> None:
    def mutate(p: dict) -> None:
        p["FloTuning"] = example("flo.tuning.bruce", "001")
        p["DispatchHold"]["OperatorHold"] = False

    default_codec.from_dict(mutated(EXAMPLE, mutate))


def test_axiom_7_a_refuses_bruce_on_house0_loop_at_lwt_control() -> None:
    def mutate(p: dict) -> None:
        p["FloTuning"] = example("flo.tuning.bruce", "001")
        p["DispatchHold"]["OperatorHold"] = False
        p["FamilyParams"]["SiegLoopStrategy"] = "LwtControl"

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 7)


def test_alice_runs_on_house0_loop_at_lwt_control() -> None:
    def mutate(p: dict) -> None:
        p["FamilyParams"]["SiegLoopStrategy"] = "LwtControl"

    default_codec.from_dict(mutated(EXAMPLE, mutate))
