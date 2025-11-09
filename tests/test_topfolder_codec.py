import pytest

from topfolder_codec import encode_topfolder, decode_topfolder


def test_encode_element():
    assert encode_topfolder("pilon", "element", "beam") == "pilon-element-beam"


def test_encode_nodal():
    assert encode_topfolder("uzli", "nodal") == "uzli-nodal"


def test_encode_none():
    assert encode_topfolder("global", "none") == "global-none"


def test_encode_invalid_user():
    with pytest.raises(ValueError):
        encode_topfolder("", "nodal")


def test_encode_missing_element_type():
    with pytest.raises(ValueError):
        encode_topfolder("p", "element")


def test_decode_element():
    assert decode_topfolder("pilon-element-beam") == ("pilon", "element", "beam")


def test_decode_nodal():
    assert decode_topfolder("uzli-nodal") == ("uzli", "nodal", None)


def test_decode_none():
    assert decode_topfolder("global-none") == ("global", "none", None)


def test_decode_with_prefix():
    assert decode_topfolder("1-uzli-nodal") == ("uzli", "nodal", None)
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
