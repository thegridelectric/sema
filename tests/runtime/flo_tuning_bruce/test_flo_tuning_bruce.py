"""flo.tuning.bruce 003: the RWT line per load bucket, proved by mutation of the example."""

from sema.runtime.codec import default_codec
from sema.runtime.types.flo_tuning_bruce import FloTuningBruce
from sema.runtime.types.old_versions.flo_tuning_bruce_001 import FloTuningBruce001
from sema.runtime.types.old_versions.flo_tuning_bruce_002 import FloTuningBruce002
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("flo.tuning.bruce", "003")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("flo.tuning.bruce", "003") == {1: [], 2: []}


def test_example_round_trips() -> None:
    t = FloTuningBruce.model_validate(EXAMPLE)
    assert FloTuningBruce.model_validate(t.model_dump(by_alias=True)) == t


def test_two_buckets_validate() -> None:
    def mutate(p: dict) -> None:
        p["LoadBucketUpperKwhList"] = [8.0]
        p["RwtInterceptByBucketList"] = [49.463, 45.0]
        p["RwtSlopeByBucketList"] = [0.427, 0.5]

    FloTuningBruce.model_validate(mutated(EXAMPLE, mutate))


def test_axiom_1_refuses_a_missing_line() -> None:
    def mutate(p: dict) -> None:
        p["LoadBucketUpperKwhList"] = [8.0]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_axiom_2_refuses_descending_bounds() -> None:
    def mutate(p: dict) -> None:
        p["LoadBucketUpperKwhList"] = [8.0, 4.0]
        p["RwtInterceptByBucketList"] = [49.463, 45.0, 40.0]
        p["RwtSlopeByBucketList"] = [0.427, 0.5, 0.6]

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 2)


def test_a_001_tuning_gains_the_unmet_load_penalty() -> None:
    old = example("flo.tuning.bruce", "001")
    upgraded = FloTuningBruce001.model_validate(old).upgrade()
    assert upgraded.version == "002"
    assert upgraded.unmet_load_penalty_enabled is False
    assert upgraded.unmet_load_penalty_weight == 10


def test_example_reads_the_unmet_load_knobs_from_experimental() -> None:
    t = FloTuningBruce.model_validate(EXAMPLE)
    assert t.experimental == {
        "UnmetLoadPenaltyEnabled": True,
        "UnmetLoadPenaltyWeight": 10.0,
    }


def test_an_empty_experimental_validates() -> None:
    def mutate(p: dict) -> None:
        p["Experimental"] = {}

    assert FloTuningBruce.model_validate(mutated(EXAMPLE, mutate)).experimental == {}


def test_a_002_tuning_moves_the_unmet_load_knobs_into_experimental() -> None:
    old = example("flo.tuning.bruce", "002")
    upgraded = FloTuningBruce002.model_validate(old).upgrade()
    assert upgraded.version == "003"
    assert upgraded.experimental == {
        "UnmetLoadPenaltyEnabled": old["UnmetLoadPenaltyEnabled"],
        "UnmetLoadPenaltyWeight": old["UnmetLoadPenaltyWeight"],
    }
    assert "UnmetLoadPenaltyEnabled" not in upgraded.model_dump(by_alias=True)
