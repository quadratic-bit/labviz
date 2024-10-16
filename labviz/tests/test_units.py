from .. import units as u
import pytest

def test_superscript():
    assert u.superscript(0) == "⁰"
    assert u.superscript(1) == ""
    assert u.superscript(-1) == "⁻¹"
    assert u.superscript(23486) == "²³⁴⁸⁶"
    assert u.superscript(-9283) == "⁻⁹²⁸³"

def test_unit_arithmetics():
    assert u.amp / u.s == u.SIValue(1.0, u.SIUnit(amp=1, s=-1))
    assert u.SIValue(2, u.SIUnit()) * u.kg / u.m ** 2 == u.SIValue(2, u.SIUnit(kg=1, m=-2))
    with pytest.raises(u.DimensionError):
        _ = u.cd + u.k
