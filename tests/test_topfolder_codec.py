import pytest

from topfolder_codec import encode_topfolder, decode_topfolder


def test_encode_element():
    assert encode_topfolder("pilon", "element", "beam") == "pilon-element-beam"


def test_encode_node():
    assert encode_topfolder("uzli", "node") == "uzli-node"


def test_encode_invalid_user():
    with pytest.raises(ValueError):
        encode_topfolder("", "node")


def test_encode_missing_element_type():
    with pytest.raises(ValueError):
        encode_topfolder("p", "element")


def test_decode_element():
    assert decode_topfolder("pilon-element-beam") == ("pilon", "element", "beam")


def test_decode_node():
    assert decode_topfolder("uzli-node") == ("uzli", "node", None)


def test_decode_with_prefix():
    assert decode_topfolder("1-uzli-node") == ("uzli", "node", None)
    assert decode_topfolder("10-pilon-element-beam") == (
        "pilon",
        "element",
        "beam",
    )


def test_decode_invalid_format():
    with pytest.raises(ValueError):
        decode_topfolder("invalid")


def test_decode_invalid_format_with_prefix():
    with pytest.raises(ValueError):
        decode_topfolder("1-invalid")


def test_decode_invalid_entity():
    with pytest.raises(ValueError):
        decode_topfolder("pilon-invalid")


def test_decode_invalid_element_type():
    with pytest.raises(ValueError):
        decode_topfolder("pilon-element-foo")
