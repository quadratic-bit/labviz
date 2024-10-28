"""Functions for creating and displaying plots compliant with the standarts."""
from typing import Iterable
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from dataclasses import dataclass
from labviz.series import Series
from labviz.errors import least_squares_error, round_on_pivot

COLOR_ROTATION = ("r", "g", "b", "y", "m", "c", "k")
color = 0
mode = ""

matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "text.usetex": False,
})

def next_color() -> str:
    """Rotates global color variable.

    Returns:
        The next color in rotation.
    """
    global color
    result = COLOR_ROTATION[color]
    color = (color + 1) % len(COLOR_ROTATION)
    return result

def ensure_mode(new_mode: str) -> None:
    """Sets matplotlib.plt mode to a new one if needed.

    Args:
        new_mode: A string containing new mode.
    """
    global mode
    if mode != new_mode:
        matplotlib.use(new_mode)
        mode = new_mode

@dataclass
class LabPlot:
    """A couple of regression coefficients, namely slope and shift.

    Attributes:
        slope: First coefficient.
        shift: Free term.
        slope_error: Random error of calculated slope
        shift_error: Random error of calculated shift
    """
    fig: Figure
    slope: float
    shift: float
    slope_error: float
    shift_error: float

def plot_and_regress(X: Series,
                     Y: Series,
                     xlabel="",
                     ylabel="",
                     locale="en") -> LabPlot:
    """Plot Y against X via matplotlib with regression line.

    Args:
        X: Series of x values.
        Y: Series of y values.
        xlabel: Label for the X axis.
        ylabel: Label for the Y axis.
        locale: SI units localization, either "en" or "ru".

    Returns:
        Regression line coefficients object.
    """
    ensure_mode("Qt5Agg")
    slope, shift = np.polyfit(X.values, Y.values, 1)
    clr = next_color()
    fig = plt.figure()
    plt.plot(X.values, Y.values, clr + "o")
    sigma_slope, sigma_shift = least_squares_error(X, Y, slope)
    sigma_k, k = round_on_pivot(sigma_slope, slope)
    sigma_b, b = round_on_pivot(sigma_shift, shift)
    plt.plot(X.values,
             shift + slope * X.values,
             clr + "-",
             lw=1,
             label=f"y = {k}x + {b}")
    plt.xlabel(
        (xlabel + ", " if xlabel else "") + X.dimension.str_locale(locale)
    )
    plt.ylabel(
        (ylabel + ", " if ylabel else "") + Y.dimension.str_locale(locale)
    )
    plt.grid(linestyle="--")
    plt.legend()
    plt.show()
    return LabPlot(fig, k, b, sigma_k, sigma_b)

def save_plot(
        fig: Figure,
        filename: str,
        extra_langs: Iterable[str] = tuple()) -> None:
    """Save plot as a pgf object.

    Args:
        fig: A figure to be saved.
        filename: Name of the resulting file.
        extra_langs: A collection of babel languages.
    """
    langs = "".join(map(lambda l: "," + l, extra_langs))
    matplotlib.rcParams.update({
        "pgf.preamble": "\n".join([
            f"\\usepackage[english{langs}]{{babel}}"
        ])
    })
    fig.savefig(filename, bbox_inches="tight")
