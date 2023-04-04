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

# %%
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import matplotlib.pyplot as plt

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

# %% [markdown]
# ## モデルのパラメータ
# ここで，問題のさまざまな物理パラメータおよび数値パラメータを定義しましょう．

# %%
elements_degree = 1

# %% [markdown]
# ## メッシュ生成

# %%
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

# %%

fb1 = mesh.outer_faces_with_direction([0.0, 0.0, 1.0], 0.01)
fb2 = mesh.outer_faces_with_direction([0.0, 0.0, -1.0], 0.01)

TOP_BOUND = 1
BOTTOM_BOUND = 2

mesh.set_region(TOP_BOUND, fb1)
mesh.set_region(BOTTOM_BOUND, fb2)

# %% [markdown]
# ## メッシュの描画
#
# メッシュをプレビューし，その妥当性を制御するために，次の手順を使用します．
# 外部グラフィカルポストプロセッサPyVistaを使用する必要があります．

# %%

mesh.export_to_vtk("mesh.vtk", "ascii")
import pyvista as pv

pv.set_plot_theme("document")
pv.start_xvfb()
pv.set_jupyter_backend("panel")

m = pv.read("mesh.vtk")
plotter = pv.Plotter()
plotter.add_mesh(m, show_edges=True)
plotter.show(cpos="zx")

# %% [markdown]
# ## 有限要素法と積分法の定義
# 有限要素法を定義します．変位フィールドを近似する最初の1つは，変位フィールドを近似する mfu です．
# これはベクトルフィールドでPythonでは次のように定義されます．

# %%

mfu = gf.MeshFem(mesh, 2)
mfu.set_classical_fem(elements_degree)
