from sema.runtime.codec import default_codec
from sema.runtime.types.new_pico import NewPico
from tests.runtime.refusal import example

EXAMPLE_100 = example("new.pico", "100")


def test_shipped_wire_shape_decodes() -> None:
    """The provisioner's announcement of a new pico."""
    decoded = default_codec.from_dict(EXAMPLE_100, auto_upgrade=False)
    assert isinstance(decoded, NewPico)
    assert decoded.hw_uid == "pico_3a202a"
