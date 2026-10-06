"""gw.element.backup 000: the element relays, non-empty and distinct."""

import pytest
from pydantic import ValidationError

from sema.runtime.types.gw_element_backup import GwElementBackup


def elements(names: list[str]) -> dict[str, object]:
    return {
        "ElementRelayNames": names,
        "InService": False,
        "TypeName": "gw.element.backup",
        "Version": "000",
    }


def test_buffer_elements_validate() -> None:
    e = GwElementBackup.model_validate(elements(["elt-buffer-top", "elt-buffer-bottom"]))
    assert not e.in_service


def test_axiom_1_no_elements() -> None:
    with pytest.raises(ValidationError, match="(?i)axiom 1"):
        GwElementBackup.model_validate(elements([]))


def test_axiom_2_an_element_listed_twice() -> None:
    with pytest.raises(ValidationError, match="(?i)axiom 2"):
        GwElementBackup.model_validate(elements(["elt-buffer-top", "elt-buffer-top"]))
