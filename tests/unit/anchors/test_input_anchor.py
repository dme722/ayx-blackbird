from ayx_blackbird.anchors import InputAnchor


def test_input_anchor_construction():
    x = InputAnchor("test", False)
    assert x.name == "test"
    assert not x.optional

    y = InputAnchor("test2", True)
    assert y.name == "test2"
    assert y.optional
