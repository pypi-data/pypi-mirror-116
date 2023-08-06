import pytest
from soiltex.conversion import texture, texture_name, usda_names


def test_texture_name_has_obvious_cases():
    assert texture_name(1, 0) == 'clay'
    assert texture_name(0, 1) == 'sand'
    assert texture_name(0, 0) == 'silt'


def test_texture_is_reversible():
    for name in usda_names:
        clay, sand = texture(name)
        assert texture_name(clay, sand) == name


def test_texture_raises_error_if_unknown():
    with pytest.raises(KeyError):
        _ = texture("walou")


def test_texture_name_raises_error_if_bad_texture():
    with pytest.raises(UserWarning):
        _ = texture_name(0.5, 0.6)  # sum > 1
    with pytest.raises(UserWarning):
        _ = texture_name(-0.5, 0.6)  # clay < 0
    with pytest.raises(UserWarning):
        _ = texture_name(0.5, -0.6)  # clay < 0
