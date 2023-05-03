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

# %% [markdown]
# # Lagrangian補間とGauss求積による面積計算

# %% [code]
import sympy as sym
from myst_nb import glue

xi, eta = sym.symbols("xi eta")

N1 = 1.0 / 4.0 * (1.0 - xi) * (1.0 - eta)
glue("N1", N1)
N2 = 1.0 / 4.0 * (1.0 + xi) * (1.0 - eta)
glue("N2", N2)
N3 = 1.0 / 4.0 * (1.0 + xi) * (1.0 + eta)
glue("N3", N3)
N4 = 1.0 / 4.0 * (1.0 - xi) * (1.0 + eta)
glue("N4", N4)

# %% [code]
_ = sym.diff(N1, xi)
_ = sym.diff(N2, xi)
_ = sym.diff(N3, xi)
_ = sym.diff(N4, xi)
_ = sym.diff(N1, eta)
_ = sym.diff(N2, eta)
_ = sym.diff(N3, eta)
_ = sym.diff(N4, eta)

glud("sym.diff(N1, xi)", sym.diff(N1, xi))
glud("sym.diff(N2, xi)", sym.diff(N2, xi))
glud("sym.diff(N3, xi)", sym.diff(N3, xi))
glud("sym.diff(N4, xi)", sym.diff(N4, xi))
glud("sym.diff(N1, eta)", sym.diff(N1, eta))
glud("sym.diff(N2, eta)", sym.diff(N2, eta))
glud("sym.diff(N3, eta)", sym.diff(N3, eta))
glud("sym.diff(N4, eta)", sym.diff(N4, eta))

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
detJ = sym.diff(x, xi) * sym.diff(y, eta) - sym.diff(y, xi) * sym.diff(x, eta)
glue("|J|", detJ)

# %% [code]
glue("sym.diff(x, xi)", sym.diff(x, xi))

# %% [code]
glue("sym.diff(y, eta)", sym.diff(y, eta))

# %% [code]
glue("sym.diff(y, xi)", sym.diff(y, xi))

# %% [code]
glue("sym.diff(x, eta)", sym.diff(x, eta))

# %% [code]
sym.expand(detJ)

# %% [code]
sym.expand(detJ).coeff(xi, 1)

# %% [code]
sym.expand(detJ).coeff(eta, 1)

# %% [code]
sym.expand(detJ).coeff(xi, 0).coeff(eta, 0)