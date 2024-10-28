LabViz
------
![coverage](./media/coverage.svg)
A tool to assist in recording and visualizing lab data

### Building

To build LabViz, follow these commands:
```sh
git clone https://github.com/quadratic-bit/labviz
cd labviz
pip install -r requirements.txt
pip install --upgrade build
python3 -m build
```

### Installation

After the building, the installation is as simple as follows:
```sh
pip install ./labviz/
```

### Usage

Here's a sample usage of LabViz:
```python
from labviz.series import Series
from labviz.plotter import plot_and_regress, save_plot
from labviz.errors import least_squares_error, round_on_pivot
import labviz.units as u

periods = Series(u.s, [...])
lengths = Series(u.m, [...])

k = 4.05e-4 * u.m ** 2 * u.s ** -2
mass = (1.527 + 1.0264) * u.kg

moments = mass * k * periods ** 2
offsets = (lengths * 0.5 / 100) ** 2

reg = plot_and_regress(offsets, moments, xlabel="h^2", ylabel="I", locale="ru")

a, b = reg.shift, reg.slope
a_error, b_error = reg.shift_error, reg.slope_error

save_plot(reg.fig, "plot.pgf", extra_langs=["russian"])
```

### Contacts
Антончиков Артём Денисович, Б05-401, antonchikov.ad@phystech.edu

### Supported Python versions
| Python        | >= 3.9             | < 3.9   |
| ------------: | :----------------: | :-----: |
| Is supported? | :white_check_mark: |   :x:   |
