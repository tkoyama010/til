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
# # GetFEMの積分点確認
#
# このノートではGetFEMの積分点を確認します。

# %% [markdown]
# ## 初期化
#
# GetFEM と NumPy をグローバルにインポートします。

# %%
import getfem as gf
import numpy as np

# %% [markdown]
# ## メッシュ生成
#
# GetFEM には，ここで説明するいくつかの制約のあるメッシュ機能があります．
# ここではそれらを使用するつもりです．

# %%
mesh = gf.Mesh("cartesian", [0.0, 1.0])
print(mesh)

# %% [markdown]
# ## メッシュの描画
#
# メッシュをプレビューし，その妥当性を制御するために，次の手順を使用します．

# %%
import pyvista as pv

pv.start_xvfb()
pv.set_jupyter_backend("panel")

mesh.export_to_vtk("mesh.vtk", "ascii")
m = pv.read("mesh.vtk")

plotter = pyvista.Plotter()
plotter.add_mesh(m)
plotter.show(cpos="xy")
