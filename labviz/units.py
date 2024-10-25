"""A set of classes for working with SI units."""
from __future__ import annotations
from dataclasses import dataclass

SUPERSCRIPT = "⁰¹²³⁴⁵⁶⁷⁸⁹"

def superscript(number: int) -> str:
    """Converts an integer representing power into a readable superscript.

    Explicitly, returns an empty string if `number` is 1 and returns a string
    containing `number`'s superscript otherwise.

    Args:
        number: A number to be converted.

    Returns:
        A string, containing a number as an integer power (superscript).
        For example,

        ```python
        assert u.superscript(0) == "⁰"
        assert u.superscript(1) == ""
        assert u.superscript(3) == "³"
        assert u.superscript(-1) == "⁻¹"
        ```
    """
    if number == -1: # avoid calling superscript(1)
        return "⁻¹"
    if number < 0:
        return "⁻" + superscript(-number)
    if number == 1:
        return ""
    result = ""
    for digit in str(number):
        result += SUPERSCRIPT[int(digit)]
    return result

LOCALIZATION = {
    "en": {
        "s": "s",
        "m": "m",
        "kg": "kg",
        "A": "A",
        "K": "K",
        "mol": "mol",
        "cd": "cd",
    },
    "ru": {
        "s": "с",
        "m": "м",
        "kg": "кг",
        "A": "А",
        "K": "К",
        "mol": "моль",
        "cd": "кд",
    }
}

class DimensionError(Exception):
    """Illegal operations with dimensions."""
    pass

@dataclass(frozen=True, kw_only=True)
class SIUnit:
    """An array representing SI dimensions.

    Attributes:
        s: A second.
        m: A meter.
        kg: A kilogram.
        amp: An ampere.
        k: A kelvin.
        mol: A mole.
        cd: A candela.
    """

    s: int = 0
    m: int = 0
    kg: int = 0
    amp: int = 0
    k: int = 0
    mol: int = 0
    cd: int = 0

    def str_locale(self, locale: str) -> str:
        """Convert the set of units into a human-readable string.

        Args:
            locale: One of the implemented locale strings
              (currently, "en" or "ru").
        """
        # TODO: handle derived units
        result = []
        for unit in ((self.s, "s"),
                     (self.m, "m"),
                     (self.kg, "kg"),
                     (self.amp, "A"),
                     (self.k, "K"),
                     (self.mol, "mol"),
                     (self.cd, "cd")):
            if unit[0] != 0:
                result.append(LOCALIZATION[locale][unit[1]] + \
                        superscript(unit[0]))
        return "·".join(result)

    def __str__(self) -> str:
        return self.str_locale("en")

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
    """A floating point value associated with SI dimensions.

    Attributes:
        value: A floating point value.
        dimension: SI dimension.
    """

    def __init__(self, value: float, dimension: SIUnit):
        """Initializes instance based on value and dimension.

        Args:
            value: A floating point number.
            dimension: An object representing value's SI unit.
        """
        self.value = value
        self.dimension = dimension

    # TODO: type annotations
    def __mul__(self, other: object, /):
        if isinstance(other, SIValue):
            return SIValue(self.value * other.value,
                           self.dimension * other.dimension)
        elif not isinstance(other, float) and not isinstance(other, int):
            return NotImplemented
        return SIValue(self.value * other, self.dimension)

    def __rmul__(self, other: object, /):
        return self * other

    def __truediv__(self, other: object, /):
        if isinstance(other, SIValue):
            return SIValue(self.value / other.value,
                           self.dimension / other.dimension)
        elif not isinstance(other, float) and not isinstance(other, int):
            return NotImplemented
        return SIValue(self.value / other, self.dimension)

    def __add__(self, other: SIValue, /) -> SIValue:
        if self.dimension != other.dimension:
            raise DimensionError(
                    "Cannot add two SI values with unequal dimensions"
            )
        return SIValue(self.value + other.value, self.dimension)

    def __sub__(self, other: SIValue, /) -> SIValue:
        if self.dimension != other.dimension:
            raise DimensionError(
                    "Cannot subtract two SI values with unequal dimensions"
            )
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
