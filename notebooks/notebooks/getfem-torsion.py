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
