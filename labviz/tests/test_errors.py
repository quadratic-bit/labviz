from labviz.errors import round_on_pivot

def test_pivot_normalization():
    assert round_on_pivot(0.0039937, 34.17520028) == (0.004, 34.175)
    assert round_on_pivot(0.0399375, 34.17520028) == (0.040, 34.180)
    assert round_on_pivot(0.3993753, 34.17520028) == (0.400, 34.200)
    assert round_on_pivot(3.9937569, 34.17520028) == (4.000, 34.000)
    assert round_on_pivot(39.937539, 34.17520028) == (40.00, 30.000)
