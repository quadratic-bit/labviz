import labviz.units as u
from labviz.series import Series

def test_series_arithmetics():
    assert Series(u.s, [0.2, 0.5, 0.9]) * 2 == Series(u.s, [0.4, 1.0, 1.8])
    assert Series(u.m * u.kg, [0.6, 27.0]) / 3 == Series(u.m * u.kg, [0.2, 9.0])
    assert Series(u.kg, [1, 4]) ** 2 == Series(u.kg ** 2, [1, 16])
