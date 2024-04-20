import getfem as gf
import numpy as np
import pyvista as pv
import streamlit as st
from stpyvista import stpyvista

elements_degree = st.sidebar.number_input('次数', min_value=1, max_value=2, value=1, step=1)
E = st.sidebar.number_input('ヤング率(N/mm^2)', value=200.0e03)
nu = st.sidebar.number_input('ポアソン比', value=0.3)
d = st.sidebar.number_input('直径(mm)', value=100.0)
T = st.sidebar.number_input('トルク(N mm)', value=1.0e06)
TOP_BOUND = 1
BOTTOM_BOUND = 2

mesh = gf.Mesh("load", "mesh.msh")

fb1 = mesh.outer_faces_with_direction([0.0, 0.0, 1.0], 0.01)
fb2 = mesh.outer_faces_with_direction([0.0, 0.0, -1.0], 0.01)

TOP_BOUND = 1
BOTTOM_BOUND = 2

mesh.set_region(TOP_BOUND, fb1)
mesh.set_region(BOTTOM_BOUND, fb2)

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
# ここで， `3` はベクトル場の次元を表します．2行目は，使用する有限要素を設定します．
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
# 以下の `add_isotropic_linearized_elasticity_brick` によって追加されている[定義済みのブリック](https://getfem.readthedocs.io/ja/latest/userdoc/model_linear_elasticity.html)を使用します．
# この追加を接線線形システムに対して行います．
# このモデルブリックを使用するために， Lamé 係数に対応するデータは，最初にモデルに追加する必要があります．
# ここでは， Lamé 係数は，領域に対して一定です．
# 以下のプログラムは，全体の弾性変形方程式を考慮に入れることができます．

# %% [code]
md.add_isotropic_linearized_elasticity_pstress_brick(mim, "u", "data_E", "data_nu")

# %% [markdown]
# 下側の境界に Dirichlet 条件を規定するために，既定のブリックを使用します．
# Dirichlet条件を定義するいくつかのオプションがあります( [Dirichlet条件ブリック要素](https://getfem.readthedocs.io/ja/latest/userdoc/model_dirichlet.html#ud-model-dirichlet) を参照)．
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

# %% [code]
md.add_initialized_data("r2", [0.0, 0.0, 0.0])
md.add_initialized_data("H2", [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
md.add_generalized_Dirichlet_condition_with_multipliers(
    mim, "u", mfu, BOTTOM_BOUND, "r2", "H2"
)

tau = 16.0 * T / np.pi / d**3
radius = d / 2.0

md.add_linear_term(
    mim, str(tau / radius) + "*" + "[-X(2), X(1), 0.0].Test_u", TOP_BOUND
)

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
