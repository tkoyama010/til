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
# # GetFEMによる丸棒のねじり解析
#
#
# 半径方向の単位ベクトル $P$ は以下の式であらわされる。
#
# $$
# P＝\begin{pmatrix}\cos \theta &\sin \theta \end{pmatrix}
# $$
#
# ベクトル $P$ を角度 $\theta$ で微分すると接線方向の単位ベクトルを得ることができる。
#
# $$
# \frac{dP}{d\theta }=\begin{pmatrix}-\sin \theta &\cos \theta \end{pmatrix}
# $$

# %%
import getfem as gf

# %% [markdown]
# ## メッシュの作成
# 今回のメッシュはPyVistaを使用して作成します。

# %%
import pyvista as pv
import numpy as np
from pyvista.examples import cells as example_cells, plot_cell

pv.start_xvfb()
pv.set_jupyter_backend("panel")

grid = pv.CylinderStructured(
    radius=np.linspace(0.0, 1.0, 2), theta_resolution=4, z_resolution=2
)
example_cells.plot_cell(grid)

# %% [markdown]
# ## メッシュの作成
# 今回のメッシュはPyVistaを使用して作成します。

# %%
import pyvista as pv
import numpy as np
from pyvista.examples import cells as example_cells, plot_cell

pv.start_xvfb()
pv.set_jupyter_backend("panel")

grid = pv.CylinderStructured(
    radius=np.linspace(0.0, 50.0, 8), height=500.0, theta_resolution=16, z_resolution=25
)
example_cells.plot_cell(grid)

# %%
import getfem as gf
import numpy as np
import pyvista as pv

pv.set_plot_theme("document")

###############################################################################
# Numerical parameters

d = 0.100  # m
L = 0.500  # m

###############################################################################
# Mesh generation.

mesh = gf.Mesh("empty", 3)

rhos = np.linspace(0.0, d / 2, 8 + 1)
phis = np.linspace(0.0, 2.0 * np.pi, 16 + 1)
zs = np.linspace(0.0, L, 25 + 1)

rho_as = rhos[:-1]
rho_bs = rhos[1:]
phi_as = phis[:-1]
phi_bs = phis[1:]
z_as = zs[:-1]
z_bs = zs[1:]

for z_a, z_b in zip(z_as, z_bs):
    for phi_a, phi_b in zip(phi_as, phi_bs):
        mesh.add_convex(
            gf.GeoTrans("GT_PRISM(3,1)"),
            [
                [
                    0,
                    d / 16 * 1 * np.cos(phi_a),
                    d / 16 * 1 * np.cos(phi_b),
                    0,
                    d / 16 * 1 * np.cos(phi_a),
                    d / 16 * 1 * np.cos(phi_b),
                ],
                [
                    0,
                    d / 16 * 1 * np.sin(phi_a),
                    d / 16 * 1 * np.sin(phi_b),
                    0,
                    d / 16 * 1 * np.sin(phi_a),
                    d / 16 * 1 * np.sin(phi_b),
                ],
                [z_a, z_a, z_a, z_b, z_b, z_b],
            ],
        )
        for rho_a, rho_b in zip(rho_as, rho_bs):
            mesh.add_convex(
                gf.GeoTrans("GT_QK(3,1)"),
                [
                    [
                        rho_a * np.cos(phi_a),
                        rho_a * np.cos(phi_b),
                        rho_b * np.cos(phi_a),
                        rho_b * np.cos(phi_b),
                        rho_a * np.cos(phi_a),
                        rho_a * np.cos(phi_b),
                        rho_b * np.cos(phi_a),
                        rho_b * np.cos(phi_b),
                    ],
                    [
                        rho_a * np.sin(phi_a),
                        rho_a * np.sin(phi_b),
                        rho_b * np.sin(phi_a),
                        rho_b * np.sin(phi_b),
                        rho_a * np.sin(phi_a),
                        rho_a * np.sin(phi_b),
                        rho_b * np.sin(phi_a),
                        rho_b * np.sin(phi_b),
                    ],
                    [z_a, z_a, z_a, z_a, z_b, z_b, z_b, z_b],
                ],
            )

mesh.export_to_vtk("mesh.vtk", "ascii")

m = pv.read("mesh.vtk")
plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(m, show_edges=True)
plotter.show(screenshot="mesh.png")
