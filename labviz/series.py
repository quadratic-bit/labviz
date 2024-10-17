from __future__ import annotations
import units as u
import numpy as np
import numpy.typing as npt

class Series:
    def __init__(self, base_unit: u.SIUnit | u.SIValue, values: npt.ArrayLike):
        if isinstance(base_unit, u.SIValue):
            self.dimension = base_unit.dimension
        else:
            self.dimension = base_unit
        self.values = np.asarray(values, dtype=np.float32)

    def __mul__(self, other: u.SIValue | float, /) -> Series:
        if isinstance(other, u.SIValue):
            return Series(self.dimension * other.dimension,
                          self.values * other.value)
        return Series(self.dimension, self.values * other)

    def __rmul__(self, other: u.SIValue | float, /) -> Series:
        return self.__mul__(other)

    def __truediv__(self, other: u.SIValue | float, /) -> Series:
        if isinstance(other, u.SIValue):
            return Series(self.dimension / other.dimension,
                          self.values / other.value)
        return Series(self.dimension, self.values / other)

    def __pow__(self, other: int, /) -> Series:
        return Series(self.dimension ** other, self.values ** other)

    def __eq__(self, other: object, /) -> bool:
        return type(other) == Series and \
                self.values == other.values and \
                self.dimension == other.dimension

    def __str__(self) -> str:
        return str(self.values)

    def __repr__(self) -> str:
        label = "series"
        lines = f"{label}({self.values}, units={self.dimension})".split("\n")
        for i in range(1, len(lines)):
            lines[i] = " " * (len(label) + 1) + lines[i]
        return "\n".join(lines)
