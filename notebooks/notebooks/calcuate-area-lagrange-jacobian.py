# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
# ---

# %% [code]
import sympy as sym
from myst_nb import glue

xi, eta = sym.symbols("xi eta")

N1 = 1.0 / 4.0 * (1.0 - xi) * (1.0 + eta)
glue("N1", N1)
N2 = 1.0 / 4.0 * (1.0 - xi) * (1.0 + eta)
glue("N2", N2)
N3 = 1.0 / 4.0 * (1.0 - xi) * (1.0 + eta)
glue("N3", N3)
N4 = 1.0 / 4.0 * (1.0 - xi) * (1.0 + eta)
glue("N4", N4)

# %% [code]
x1, x2, x3, x4 = sym.symbols("x_{1} x_{2} x_{3} x_{4}")
y1, y2, y3, y4 = sym.symbols("y_{1} y_{2} y_{3} y_{4}")

# %% [code]

x = N1 * x1 + N2 * x2 + N3 * x3 + N4 * x4
glue("x", x)
y = N1 * y1 + N2 * y2 + N3 * y3 + N4 * y4
glue("y", y)

# %% [code]

J = sym.Matrix(
    [[sym.diff(x, xi), sym.diff(y, xi)], [sym.diff(x, eta), sym.diff(y, eta)]]
)
glue("J", J)

# %% [code]
sym.expand(detJ)

# %% [code]
detJ = sym.diff(x, xi) * sym.diff(y, eta) - sym.diff(y, xi) * sym.diff(x, eta)
glue("|J|", detJ)
