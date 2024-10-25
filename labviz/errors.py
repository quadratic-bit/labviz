"""Functions for calculating errors and rounding numbers."""
from labviz.series import Series
import numpy as np
import math

# TODO: make slope optional
def least_squares_error(X: Series,
                        Y: Series,
                        slope: float) -> tuple[float, float]:
    """Computes error for least square regression coefficients.

    Args:
        X: Series of x values.
        Y: Series of y values.
        slope: Calculated slope based on provided X and Y.

    Returns:
        A tuple of calculated errors, `(sigma_slope, sigma_shift)`.
    """
    length = len(X.values)
    assert length == len(Y.values)
    x = X.values
    y = Y.values
    denominator = (x ** 2).mean() - x.mean() ** 2
    sigma_slope = np.sqrt(
        ( (y ** 2).mean() - y.mean() ** 2 ) /
        denominator - slope ** 2
    ) / np.sqrt(length)
    sigma_shift = sigma_slope * np.sqrt(denominator)
    return (sigma_slope, sigma_shift)

def round_on_pivot(pivot: float, value: float) -> tuple[float, float]:
    """Apply scientific rounding.

    Round pivot based on its first significant digit and then round value
    based on this number.

    Args:
        pivot: A floating point number dictating rounding places needed.
        value: A floating point number rounded based on pivot.

    Returns:
        A tuple of rounded numbers, `(pivot, value)`.
    """
    abs_pivot = abs(pivot)
    abs_value = abs(value)
    shift = int(math.log10(abs_pivot))

    rounded_pivot: float
    rounded_value: float
    if abs_pivot < 1:
        rounded_pivot = round(abs_pivot, -shift + 1)
        rounded_value = round(abs_value, -shift + 1)
    else:
        rounded_pivot = round(abs_pivot * 10 ** (-shift)) * 10 ** shift
        rounded_value = round(abs_value * 10 ** (-shift)) * 10 ** shift

    return (math.copysign(rounded_pivot, pivot),
            math.copysign(rounded_value, value))
