LabViz architecture
-------------------

### Problem statement
Consider the following python code for visualizing lab data within an
experiment:
```python
periods = np.array([0.00039965991178427399 * (1.527 + 1.0264) * T2 for T2 in (np.array([61.8, 61.95, 62.42, 62.855, 63.55, 64.55, 65.66, 67.17, 68.82, 70.78, 72.68, 74.9, 77.25, 79.85, 81.965, 84.71], dtype=np.float64) / 20) ** 2])
offsets = np.array([i * 0.5 / 100 for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]], dtype=np.float64) ** 2

bup1, mup1 = np.polyfit(offsets, periods, 1)
print(bup1, mup1)

plt.plot(offsets, periods, "ro")
plt.plot(offsets, mup1 + bup1 * offsets, "r-", lw=1, label="y = 1.527x + 0.010")
print(np.sqrt(
        (sum(periods ** 2) / len(periods) - (sum(periods) / len(periods)) ** 2) /
        (sum(offsets ** 2) / len(offsets) - (sum(offsets) / len(offsets)) ** 2)
        - bup1 ** 2
    ) / np.sqrt(len(periods)))

plt.xlabel("$h^2$, м$^2$")
plt.ylabel("$I$, кг*м$^2$")
plt.grid(linestyle="--")
plt.legend()
plt.show()
```
As can be seen above, data input and post-processing appears to be cumbersome
and cluttered, so some sort of pipeline needs to be introduced. Another problem
is code duplication between different lab experiments, which leads to
quite ambiguous variables' names (see, `bup1`, `mup1`, `periods`). There are
also constants present inside strings which are in zero ways connected to the
data they were derived from (see, `label="y = 1.527x + 0.010"`), so they get
outdated as soon as original data mutates.

Let's look at the surrounding logic:
```python

#matplotlib.use("Qt5Agg")
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "text.usetex": False,
    "pgf.preamble": "\n".join([
        r"\usepackage[T2A]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[english,russian]{babel}"
    ])
})

...

#plt.show()
plt.savefig("plot1.pgf", bbox_inches="tight")
```
Presented boilerplate should be extracted and handled in a more fine-grained
manner. There's also the "switch" between data viz and export for the report,
which can and should be simplified.

### Tool overview

This tool is intended for data visualization in a format compliant with
_standards_&trade; described
[here](https://old.mipt.ru/education/chair/physics/S_I/lab/requirements18.pdf)
(to be translated and formalized).
The foreseeable ways of interaction with the tool are:
1. Library
2. Console application

#### Library
The library part should expose all the necessary classes and methods to
(as concisely as possible) label, handle, reuse, post-process and plot
laboratory data.

Post-processing part might be realized through wrapping various useful NumPy
array methods, e.g., for applying some physics formula to a data series.

Handling part should include all the instruments to apply correct
rounding and scientific formatting of chosen values. Another way of handling
might include derivation, simplification and presentation of all measurement
units.

Plotting part must include feature of adding regression in the form of
NumPy's `.polyfit` (least squares), as well as extracting the coefficients and
treating them according to the _standards_&trade;.

#### Console application
The "console application" part (read, CLI tool) should expose an interactive
prompt with a set of commands binding a simple logic for adding, deleting, etc.
raw laboratory data (test points) and real-time plotting of the result
(for the purpose of finding outlying points). The output of the resulting data
series might be implemented via `stdout` using Python syntax for object
formatting.

### Dependencies
- Matplotlib
- NumPy
