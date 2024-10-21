import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from dataclasses import dataclass
from labviz.series import Series
from labviz.errors import least_squares_error, round_on_pivot

COLOR_ROTATION = ("r", "g", "b", "y", "m", "c", "k")
color = 0
mode = ""

def next_color() -> str:
    global color
    result = COLOR_ROTATION[color]
    color = (color + 1) % len(COLOR_ROTATION)
    return result

def ensure_mode(new_mode: str):
    global mode
    if mode != new_mode:
        matplotlib.use(new_mode)
        mode = new_mode

@dataclass
class RegressionCoefficients:
    slope: float
    shift: float

# TODO: multiple plots
def plot_and_regress(X: Series, Y: Series, xlabel="", ylabel="", locale="en") -> RegressionCoefficients:
    ensure_mode("Qt5Agg")
    slope, shift = np.polyfit(X.values, Y.values, 1)
    clr = next_color()
    plt.plot(X.values, Y.values, clr + "o")
    sigma_slope, sigma_shift = least_squares_error(X, Y, slope)
    k = round_on_pivot(sigma_slope, slope)[1]
    b = round_on_pivot(sigma_shift, shift)[1]
    plt.plot(X.values, shift + slope * X.values, clr + "-", lw=1, label=f"y = {k}x + {b}")
    plt.xlabel((xlabel + ", " if xlabel else "") + X.dimension.str_locale(locale))
    plt.ylabel((ylabel + ", " if ylabel else "") + Y.dimension.str_locale(locale))
    plt.grid(linestyle="--")
    plt.legend()
    plt.show()
    return RegressionCoefficients(slope, shift)
