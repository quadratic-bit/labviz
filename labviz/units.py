from __future__ import annotations
from dataclasses import dataclass

SUPERSCRIPT = "⁰¹²³⁴⁵⁶⁷⁸⁹"

def superscript(number: int) -> str:
    if number < 0:
        return "⁻" + superscript(-number)
    if number == 1:
        return ""
    result = ""
    for digit in str(number):
        result += SUPERSCRIPT[int(digit)]
    return result

class DimensionError(Exception):
    pass

@dataclass(frozen=True, kw_only=True)
class SIUnit:
    s: int = 0
    m: int = 0
    kg: int = 0
    amp: int = 0
    k: int = 0
    mol: int = 0
    cd: int = 0

    def __str__(self) -> str:
        # TODO: handle derived units
        result = []
        if self.s != 0:
            result.append("s" + superscript(self.s))
        if self.m != 0:
            result.append("m" + superscript(self.m))
        if self.kg != 0:
            result.append("kg" + superscript(self.kg))
        if self.amp != 0:
            result.append("A" + superscript(self.amp))
        if self.k != 0:
            result.append("K" + superscript(self.k))
        if self.mol != 0:
            result.append("mol" + superscript(self.mol))
        if self.cd != 0:
            result.append("cd" + superscript(self.cd))
        return "·".join(result)

    def __mul__(self, other: SIUnit, /) -> SIUnit:
        return SIUnit(s   = self.s   + other.s,
                      m   = self.m   + other.m,
                      kg  = self.kg  + other.kg,
                      amp = self.amp + other.amp,
                      k   = self.k   + other.k,
                      mol = self.mol + other.mol,
                      cd  = self.cd  + other.cd)

    def __truediv__(self, other: SIUnit, /) -> SIUnit:
        return SIUnit(s   = self.s   - other.s,
                      m   = self.m   - other.m,
                      kg  = self.kg  - other.kg,
                      amp = self.amp - other.amp,
                      k   = self.k   - other.k,
                      mol = self.mol - other.mol,
                      cd  = self.cd  - other.cd)

    def __pow__(self, other: int, /) -> SIUnit:
        return SIUnit(s   = self.s   * other,
                      m   = self.m   * other,
                      kg  = self.kg  * other,
                      amp = self.amp * other,
                      k   = self.k   * other,
                      mol = self.mol * other,
                      cd  = self.cd  * other)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"

class SIValue:
    def __init__(self, value: float, dimension: SIUnit):
        self.value = value
        self.dimension = dimension

    def __mul__(self, other: SIValue, /) -> SIValue:
        return SIValue(self.value * other.value,
                       self.dimension * other.dimension)

    def __truediv__(self, other: SIValue, /) -> SIValue:
        return SIValue(self.value / other.value,
                       self.dimension / other.dimension)

    def __add__(self, other: SIValue, /) -> SIValue:
        if self.dimension != other.dimension:
            raise DimensionError("Cannot add two SI values with unequal dimensions")
        return SIValue(self.value + other.value, self.dimension)

    def __sub__(self, other: SIValue, /) -> SIValue:
        if self.dimension != other.dimension:
            raise DimensionError("Cannot subtract two SI values with unequal dimensions")
        return SIValue(self.value - other.value, self.dimension)

    def __pow__(self, other: int, /) -> SIValue:
        return SIValue(self.value ** other, self.dimension ** other)

    def __eq__(self, other: object, /) -> bool:
        return type(other) == SIValue and \
                self.value == other.value and \
                self.dimension == other.dimension

    def __str__(self) -> str:
        return f"{self.value} {self.dimension}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"

s   = SIValue(1.0, SIUnit(s=1))
m   = SIValue(1.0, SIUnit(m=1))
kg  = SIValue(1.0, SIUnit(kg=1))
amp = SIValue(1.0, SIUnit(amp=1))
k   = SIValue(1.0, SIUnit(k=1))
mol = SIValue(1.0, SIUnit(mol=1))
cd  = SIValue(1.0, SIUnit(cd=1))

# TODO: add tests
