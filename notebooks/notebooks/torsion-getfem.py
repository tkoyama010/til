# %% [code]
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
# https://github.com/matplotlib/matplotlib/issues/5836#issuecomment-179592427
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import matplotlib.pyplot as plt

!conda config --add channels conda-forge
!conda config --set channel_priority strict
!yes | mamba install getfem > log.txt
!pip install pyvista

# %% [markdown]
# # GetFEMによる丸棒のねじり解析
#
#
# 半径方向の単位ベクトル $P$ は以下の式であらわされます．
#
# $$
# P＝\begin{pmatrix}\cos \theta &\sin \theta \end{pmatrix}
# $$
#
# ベクトル $P$ を角度 $\theta$ で微分すると接線方向の単位ベクトルを得ることができます．
#
# $$
# \frac{dP}{d\theta }=\begin{pmatrix}-\sin \theta &\cos \theta \end{pmatrix}
# $$

# %% [markdown]
# ```{tikz}
# :include: torsion-getfem.tikz
# ```
# ![torsion-getfem.tikz](https://tkoyama010-notebooks--43.org.readthedocs.build/ja/43/_images/tikz-9f57e75ffb45fd5f55aba90909a383e1bb73b131.png "torsion-getfem.tikz")

# %% [markdown]
# ## モデルのパラメータ
# ここで，問題のさまざまな物理パラメータおよび数値パラメータを定義しましょう．

# %% [code]
elements_degree = 1

# %% [markdown]
# ## メッシュ生成

# %% [code]
import getfem as gf
import numpy as np
import pyvista as pv

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

# %% [markdown]
# ## 境界の選択
#
# 境界のそれぞれの部分には異なる境界条件を設定するため，境界のさまざまな部分には番号を付けます．
# したがって，メッシュ上の要素面を選択し，メッシュ領域を定義する必要があります．
# 1, 2はそれぞれ上境界，下境界です．
# これらの境界番号は，モデルのブリックで使用されます．

# %% [code]

fb1 = mesh.outer_faces_with_direction([0.0, 0.0, 1.0], 0.01)
fb2 = mesh.outer_faces_with_direction([0.0, 0.0, -1.0], 0.01)

TOP_BOUND = 1
BOTTOM_BOUND = 2

mesh.set_region(TOP_BOUND, fb1)
mesh.set_region(BOTTOM_BOUND, fb2)

# %% [markdown]
# ## メッシュの描画
# #
# メッシュをプレビューし，その妥当性を制御するために，次の手順を使用します．
# 外部グラフィカルポストプロセッサPyVistaを使用する必要があります．

# %% [code]
mesh.export_to_vtk("mesh.vtk", "ascii")
import pyvista as pv

pv.set_plot_theme("document")
pv.start_xvfb()
pv.set_jupyter_backend("panel")

m = pv.read("mesh.vtk")
plotter = pv.Plotter()
plotter.add_mesh(m, show_edges=True)
plotter.show(cpos="yz")

# %% [markdown]
# ```{Tip}``
# 上に示したジオメトリはインタラクティブです。
# ```

# %% [markdown]
# ## 有限要素法と積分法の定義
# 有限要素法を定義します．変位フィールドを近似する最初の1つは，変位フィールドを近似する `mfu` です．
# これはベクトルフィールドでPythonでは次のように定義されます．

# %% [code]
mfu = gf.MeshFem(mesh, 2)
mfu.set_classical_fem(elements_degree)

# %% [markdown]
# ここで， `2` はベクトル場の次元を表します．2行目は，使用する有限要素を設定します．
# `classical_finite_element` は，連続したLagrange要素を意味し， `elements_degree` は `2` に設定されています．
# これは2次の (アイソパラメトリック) 要素を使用することを意味します．
# GetFEM では，既存の有限要素法を幅広く選択肢できます．
# [付録A.有限要素法リスト](https://getfem.readthedocs.io/ja/latest/userdoc/appendixA.html#ud-appendixa) を参照してください．
# しかし，実際には Lagrange 有限要素法が最も使用されています．

# %% [markdown]
# 次に定義するのは，積分法 `mim` です． *GetFEM* にデフォルトの積分法はありません．
# したがって，これは積分法を定義するためには必須です．
# もちろん，積分法の次数は，選択された有限要素法に好都合な積分を行うため，十分に選定しなければなりません．
# ここでは，完全積分を選択します。

# %% [code]
mim = gf.MeshIm(
    mesh,
    gf.Integ(
        "IM_PRODUCT(IM_GAUSS1D("
        + str(elements_degree + 2)
        + "), IM_GAUSS1D("
        + str(elements_degree + 2)
        + "))"
    ),
)

# %% [code]
