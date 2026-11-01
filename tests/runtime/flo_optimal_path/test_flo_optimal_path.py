"""flo.optimal.path 000: the step grid and its parallel lists."""

import pytest
from pydantic import ValidationError

from sema.runtime.types.flo_optimal_path import FloOptimalPath


def path(**overrides: object) -> dict[str, object]:
    d: dict[str, object] = {
        "StartUnixS": 1762009200,
        "StepDurationMinutes": [60, 60, 60],
        "HpAvgWList": [4200, 0, 3100],
        "StoreWhList": [38500, 31200, 36800],
        "TypeName": "flo.optimal.path",
        "Version": "000",
    }
    d.update(overrides)
    return d


def test_example_validates_and_round_trips() -> None:
    p = FloOptimalPath.model_validate(path())
    assert p.hp_avg_w_list == [4200, 0, 3100]
    assert FloOptimalPath.model_validate(p.model_dump(by_alias=True)) == p


def test_zero_minute_step_is_refused() -> None:
    with pytest.raises(ValidationError):
        FloOptimalPath.model_validate(path(StepDurationMinutes=[60, 0, 60]))


def test_float_watts_are_refused() -> None:
    with pytest.raises(ValidationError):
        FloOptimalPath.model_validate(path(HpAvgWList=[4200.5, 0, 3100]))


@pytest.mark.parametrize(
    "field, value",
    [
        ("StepDurationMinutes", [60, 60]),
        ("HpAvgWList", [4200, 0]),
        ("StoreWhList", [38500, 31200, 36800, 40000]),
    ],
)
def test_axiom_1_lists_of_unequal_length(field: str, value: list[int]) -> None:
    with pytest.raises(ValidationError, match="(?i)axiom 1"):
        FloOptimalPath.model_validate(path(**{field: value}))
