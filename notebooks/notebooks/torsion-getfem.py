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

# %% [markdown]
# ## モデルのパラメータ
# ここで，問題のさまざまな物理パラメータおよび数値パラメータを定義しましょう．

# %% [code]
elements_degree = 1
E = 200.0e06  # N/m^2
nu = 0.3
d = 0.100  # m
L = 0.500  # m

# %% [markdown]
# ## 初期化
#
# Python の場合，これは簡単です．
# GetFEM をグローバルにインポートするだけです(numpy と pyvista もインポートする必要があります)．

# %% [code]
import getfem as gf
import numpy as np
import pyvista as pv

pv.start_xvfb()
pv.set_jupyter_backend("panel")

# %% [markdown]
# ## メッシュ生成
#
# GetFEMには円筒形のメッシュを作成する機能はありません．
# その代わり立方体の規則的なメッシュを素早く作成する機能があるためそれを利用します．
# NumPyの配列からX方向長さが円筒形の半径 $r$ ，Y方向長さが $2\pi$ のメッシュを作成します．
# しかしながら，この方法ではポイントのマージがうまくいかず，断念せざるを得ませんでした．
#

# %% [code]
# rhos = np.linspace(0.0001, d / 2, 8 + 1)
# phis = np.linspace(0.0, 2.0 * np.pi, 16 + 1)
# zs = np.linspace(L, 0.0, 25 + 1)
# mesh = gf.Mesh("cartesian Q1", rhos, phis, zs)
# pts = mesh.pts()
# r = pts[0]
# t = pts[1]
# z = pts[2]
# mesh.set_pts(np.array([r * np.cos(t), r * np.sin(t), z]))

# %% [markdown]
# そのため，メッシュをフルスクラッチで作成をしました．

# %% [code]
rhos = np.linspace(0.0001, d / 2, 8 + 1)
phis = np.linspace(0.0, 2.0 * np.pi, 16 + 1)
zs = np.linspace(L, 0.0, 25 + 1)
mesh = gf.Mesh("empty", 3)

rho_as = rhos[:-1]
rho_bs = rhos[1:]
phi_as = phis[:-1]
phi_bs = phis[1:]
z_as = zs[:-1]
z_bs = zs[1:]

for z_a, z_b in zip(z_as, z_bs):
    for phi_a, phi_b in zip(phi_as, phi_bs):
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
# ```{tip}
# 節点数と要素数を確認すること．
# ```

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
#
# メッシュをプレビューし，その妥当性を制御するために，次の手順を使用します．
# 外部グラフィカルポストプロセッサPyVistaを使用する必要があります．

# %% [code]
mesh.export_to_vtk("mesh.vtk", "ascii")

m = pv.read("mesh.vtk")
plotter = pv.Plotter()
plotter.add_mesh(m, show_edges=True)
plotter.enable_parallel_projection()
plotter.show(cpos="yz")

# %% [markdown]
# ```{tip}
# 上に示したジオメトリはインタラクティブです．
# また、[平行投影](https://pyvista.github.io/pyvista-docs-dev-ja/api/plotting/_autosummary/pyvista.Renderer.enable_parallel_projection.html)を有効にします．
# ```

# %% [markdown]
# ## 有限要素法と積分法の定義
#
# メッシュをプレビューし，その妥当性を制御するために，次の手順を使用します．
# 有限要素法を定義します．変位フィールドを近似する最初の1つは，変位フィールドを近似する `mfu` です．
# これはベクトルフィールドでPythonでは次のように定義されます．

# %% [code]
mfu = gf.MeshFem(mesh, 3)
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
        "IM_PRODUCT(IM_PRODUCT(IM_GAUSS1D("
        + str(elements_degree + 2)
        + "), IM_GAUSS1D("
        + str(elements_degree + 2)
        + ")), IM_GAUSS1D("
        + str(elements_degree + 2)
        + "))"
    ),
)

# %% [markdown]
# ## モデルの定義
# *GetFEM* のモデルオブジェクトは(未知)変数，データ，およびモデルブリックと呼ばれるものの集まりです．
# モデルブリックは，単一の変数か，複数の変数をリンクしているモデルの一部 (線形または非線形項) です．
# これらは，(接線) 線形システムの構築のために使用されます (詳細については
# [modelオブジェクト](https://getfem.readthedocs.io/ja/latest/userdoc/model_object.html#ud-model-object)
# を参照してください)．
#
# 計算される1つのフィールドに対応する1つの変数を持つ実際のモデルを宣言してみましょう ．

# %% [code]
md = gf.Model("real")
md.add_fem_variable("u", mfu)
md.add_initialized_data("data_E", E)
md.add_initialized_data("data_nu", nu)

# %% [markdown]
# ### 弾性変形問題
# ここでは，弾性変形問題から始めましょう．
# 以下の `add_isotropic_linearized_elasticity_brick` によって追加されている定義済みのブリックを使用します．
# 対応する項は以下の通りです．
# $$
# \int_{\Omega} (\lambda^* \mbox{div}(u) I + 2\mu \bar{\varepsilon}(u)):\bar{\varepsilon}(\delta_u)dx,
# $$
# この追加を接線線形システムに対して行います．
# このモデルブリックを使用するために， Lamé 係数に対応するデータは，最初にモデルに追加する必要があります．
# ここでは， Lamé 係数は，領域に対して一定です．
# 以下のプログラムは，全体の弾性変形方程式を考慮に入れることができます．

# %% [code]
md.add_isotropic_linearized_elasticity_pstress_brick(mim, "u", "data_E", "data_nu")

# %% [markdown]
# 下側の境界に Dirichlet 条件を規定するために，既定のブリックを使用します．
# Dirichlet条件を定義するいくつかのオプションがあります( [Dirichlet条件ブリック要素](https://getfem.readthedocs.io/ja/latest/userdoc/model_dirichlet.html#ud-model-dirichlet) を参照)．

# %% [code]
md.add_initialized_data("r2", [0.0, 0.0, 0.0])
md.add_initialized_data("H2", [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
md.add_generalized_Dirichlet_condition_with_multipliers(
    mim, "u", mfu, BOTTOM_BOUND, "r2", "H2"
)
md.add_linear_term(mim, "[-X(2), X(1), 0.0].Test_u", TOP_BOUND)

# %% [markdown]
# ## モデルの求解
# モデルを正しく定義したら，次のようにして簡単に解くことができます．

# %% [code]

md.solve()

# %% [markdown]
# ## 解のエクスポート/可視化
# 以上で有限要素問題が解けました．
# 図のように解をプロットすることができます．

# %% [code]

U = md.variable("u")
mfu.export_to_vtk("displacement.vtk", "ascii", mfu, U, "u")

d = pv.read("displacement.vtk")
plotter = pv.Plotter()
plotter.add_mesh(d.warp_by_vector("u", factor=1.0e08), show_edges=True)
plotter.enable_parallel_projection()
plotter.show(cpos="yz")

# %% [markdown]
# ```{tip}
# 上に示したジオメトリはインタラクティブです．
# また、[平行投影](https://pyvista.github.io/pyvista-docs-dev-ja/api/plotting/_autosummary/pyvista.Renderer.enable_parallel_projection.html)を有効にします．
# ```
