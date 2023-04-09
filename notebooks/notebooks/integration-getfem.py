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

plotter = pv.Plotter()
plotter.add_mesh(m)
plotter.add_mesh(
    pv.PolyData(m.points), color="red", point_size=10, render_points_as_spheres=True
)
plotter.show(cpos="xy")

# %% [markdown]
# ```{Tip}
# 上に示したジオメトリはインタラクティブです。
# ```

# %% [markdown]
# ## 積分法の定義
#
# 定義するのは積分法 `mim` です．GetFEM にデフォルトの積分法はありません．
# したがって，これは積分法を定義するためには必須です．
# もちろん，積分法の次数は，選択された有限要素法に好都合な積分を行うため，十分に選定しなければなりません．

# %%
print([(1.0 - np.sqrt(1.0 / 3.0)) / 2.0, (1.0 + np.sqrt(1.0 / 3.0)) / 2.0])

# %%
im = gf.Integ("IM_GAUSS1D(1)")
print("im")
print(im)
print("im.pts()")
print(im.pts())
print("im.coeffs()")
print(im.coeffs())

# %%
im = gf.Integ("IM_GAUSS1D(3)")
print("im")
print(im)
print("im.pts()")
print(im.pts())
print("im.coeffs()")
print(im.coeffs())

# %%
im = gf.Integ("IM_GAUSS1D(5)")
print("im")
print(im)
print("im.pts()")
print(im.pts())
print("im.coeffs()")
print(im.coeffs())

# %%
im = gf.Integ("IM_PRODUCT(IM_GAUSS1D(3), IM_GAUSS1D(3))")
print("im")
print(im)
print("im.pts()")
print(im.pts())
print("im.coeffs()")
print(im.coeffs())
