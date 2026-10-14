from sema.runtime.codec import default_codec
from sema.runtime.types.new_code import NewCode
from tests.runtime.refusal import example

EXAMPLE_100 = example("new.code", "100")


def test_shipped_wire_shape_decodes() -> None:
    """The code-update request the fleet firmware posts at boot."""
    decoded = default_codec.from_dict(EXAMPLE_100, auto_upgrade=False)
    assert isinstance(decoded, NewCode)
    assert decoded.actor_node_name == "primary-btu"
