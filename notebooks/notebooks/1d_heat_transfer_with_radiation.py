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
# # One dimensional heat transfer with radiation
#
# この問題は1次元方向の熱伝導解析で発生する温度を確認するベンチマークです。
# The Standard NAFEMS BenchmarksにT2として掲載されています。

# %% [markdown]
# # メッシュ作成

# %%
import getfem as gf
import numpy as np
import pyvista as pv

pv.set_plot_theme("document")
pv.start_xvfb()
pv.set_jupyter_backend("panel")

mesh = gf.Mesh("cartesian", np.linspace(0.0, 0.1, 10))
mesh.export_to_vtk("mesh.vtk", "ascii")

m = pv.read("mesh.vtk")
m.plot()
