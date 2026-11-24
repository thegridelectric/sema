"""cop.curve 001: the lift-based COP model, proved by mutation of the example."""

import pytest

from sema.runtime.base import UpgradeRequiresContext
from sema.runtime.codec import default_codec
from sema.runtime.types.cop_curve import CopCurve
from sema.runtime.types.old_versions.cop_curve_000 import CopCurve000
from tests.runtime.refusal import assert_refused, axioms, example, mutated

EXAMPLE = example("cop.curve", "001")


def test_every_axiom_has_a_mutation() -> None:
    assert axioms("cop.curve", "001") == {1: []}


def test_example_round_trips() -> None:
    curve = CopCurve.model_validate(EXAMPLE)
    assert curve.lwt_minus_oat_coeff <= 0
    assert curve.to_dict() == EXAMPLE


def test_a_positive_lift_coefficient_is_refused() -> None:
    def mutate(p: dict) -> None:
        p["LwtMinusOatCoeff"] = 0.01

    assert_refused(default_codec, mutated(EXAMPLE, mutate), 1)


def test_a_000_curve_is_a_different_fit_and_does_not_upgrade() -> None:
    old = CopCurve000.model_validate(example("cop.curve", "000"))
    with pytest.raises(UpgradeRequiresContext):
        old.upgrade()
