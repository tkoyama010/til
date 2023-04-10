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
# # 求積法のリスト
#
# GetFEM の積分法のリストを与えます．

# %% [markdown]
# ## 初期化
#
# GetFEM と NumPy をグローバルにインポートします。

# %%
import getfem as gf
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# ## 積分法の定義
#
# 定義するのは積分法 `im` です．GetFEM にデフォルトの積分法はありません．
# したがって，これは積分法を定義するためには必須です．
# もちろん，積分法の次数は，選択された有限要素法に好都合な積分を行うため，十分に選定しなければなりません．

# %% [markdown]
# ## 1次元のGauss積分法
# `K` 次（ `K/2+1` 点）のGauss-Legendreは， "IM_GAUSS1D(K)" と表記します．

# %%
im = gf.Integ("IM_GAUSS1D(3)")
print("im")
print(im)
print("im.pts()")
print(im.pts())
print("im.coeffs()")
print(im.coeffs())

# %%
pts = im.pts()
coeffs = im.coeffs()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([0.0, 1.0], [0.5, 0.5], color="black", linewidth=2)
ax.plot(
    pts[0],
    pts[0] * 0.0 + 0.5,
    linewidth=0,
    marker="o",
    markersize=10,
    markeredgecolor="red",
    markerfacecolor="red",
)
for x, coeff in zip(pts[0], coeffs):
    label = "{:.3f}".format(coeff)
    ax.annotate(label, (x, 0.5), xytext=(0.0, 10.0), textcoords="offset points")
ax.grid()
ax.set_xlim(-0.2, 1.2)
ax.set_xticks(
    [
        -0.2,
        0.0,
        1.0 / 2.0 * (1.0 - np.sqrt(3.0) / 3.0),
        1.0 / 2.0 * (1.0 + np.sqrt(3.0) / 3.0),
        1.0,
        1.2,
    ]
)
ax.set_xticklabels(
    [
        "",
        r"$0$",
        r"$\dfrac{1}{2}\left(1 - \dfrac{\sqrt{3}}{3}\right)$",
        r"$\dfrac{1}{2}\left(1 + \dfrac{\sqrt{3}}{3}\right)$",
        r"$1$",
        "",
    ]
)
ax.set_ylim(-0.2, 1.2)
ax.set_yticks([-0.2, 0.5, 1.2])
ax.set_yticklabels(
    [
        "",
        "",
        "",
    ]
)
plt.show()

# %% [markdown]
# ## 積分法の直積
# `"IM_PRODUCT(IM1, IM2)"` を使って，4辺形やプリズムの積分法を作ることができます．

# %%
im = gf.Integ("IM_PRODUCT(IM_GAUSS1D(3), IM_GAUSS1D(3))")
print("im")
print(im)
print("im.pts()")
print(im.pts())
print("im.coeffs()")
print(im.coeffs())

# %%
pts = im.pts()
coeffs = im.coeffs()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(
    [0.0, 1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0, 0.0], color="black", linewidth=2
)
ax.plot(
    pts[0],
    pts[1],
    linewidth=0,
    marker="o",
    markersize=10,
    markeredgecolor="red",
    markerfacecolor="red",
)
for x, y, coeff in zip(pts[0], pts[1], coeffs):
    label = "{:.3f}".format(coeff)
    ax.annotate(label, (x, y), xytext=(0.0, 10.0), textcoords="offset points")
ax.grid()
ax.set_xlim(-0.2, 1.2)
ax.set_xticks(
    [
        -0.2,
        0.0,
        1.0 / 2.0 * (1.0 - np.sqrt(3.0) / 3.0),
        1.0 / 2.0 * (1.0 + np.sqrt(3.0) / 3.0),
        1.0,
        1.2,
    ]
)
ax.set_xticklabels(
    [
        "",
        r"$0$",
        r"$\dfrac{1}{2}\left(1 - \dfrac{\sqrt{3}}{3}\right)$",
        r"$\dfrac{1}{2}\left(1 + \dfrac{\sqrt{3}}{3}\right)$",
        r"$1$",
        "",
    ]
)
ax.set_ylim(-0.2, 1.2)
ax.set_yticks(
    [
        -0.2,
        0.0,
        1.0 / 2.0 * (1.0 - np.sqrt(3.0) / 3.0),
        1.0 / 2.0 * (1.0 + np.sqrt(3.0) / 3.0),
        1.0,
        1.2,
    ]
)
ax.set_yticklabels(
    [
        "",
        r"$0$",
        r"$\dfrac{1}{2}\left(1 - \dfrac{\sqrt{3}}{3}\right)$",
        r"$\dfrac{1}{2}\left(1 + \dfrac{\sqrt{3}}{3}\right)$",
        r"$1$",
        "",
    ]
)
plt.show()

# %% [markdown]
# ## 検算
#
# isoparametric座標と全体座標が一致する場合に負担面積が適切に計算されるか確認を行います。
# まず、節点1から節点4の形状関数を定義します。


# %%
def N1(epsilon, eta):
    return 1.0 / 2.0 * (1.0 - epsilon) * (1.0 - eta)


def N2(epsilon, eta):
    return 1.0 / 2.0 * (1.0 + epsilon) * (1.0 - eta)


def N3(epsilon, eta):
    return 1.0 / 2.0 * (1.0 + epsilon) * (1.0 + eta)


def N4(epsilon, eta):
    return 1.0 / 2.0 * (1.0 - epsilon) * (1.0 + eta)


# %% [markdown]
# それぞれの形状関数から負担面積はGauss積分により以下の通り計算されます。

# %%
A1 = np.sum(
    [
        1.0 * N1(-np.sqrt(3) / 3, -np.sqrt(3) / 3),
        1.0 * N1(-np.sqrt(3) / 3, np.sqrt(3) / 3),
        1.0 * N1(np.sqrt(3) / 3, -np.sqrt(3) / 3),
        1.0 * N1(np.sqrt(3) / 3, np.sqrt(3) / 3),
    ]
)
A2 = np.sum(
    [
        1.0 * N2(-np.sqrt(3) / 3, -np.sqrt(3) / 3),
        1.0 * N2(-np.sqrt(3) / 3, np.sqrt(3) / 3),
        1.0 * N2(np.sqrt(3) / 3, -np.sqrt(3) / 3),
        1.0 * N2(np.sqrt(3) / 3, np.sqrt(3) / 3),
    ]
)
A3 = np.sum(
    [
        1.0 * N3(-np.sqrt(3) / 3, -np.sqrt(3) / 3),
        1.0 * N3(-np.sqrt(3) / 3, np.sqrt(3) / 3),
        1.0 * N3(np.sqrt(3) / 3, -np.sqrt(3) / 3),
        1.0 * N3(np.sqrt(3) / 3, np.sqrt(3) / 3),
    ]
)
A4 = np.sum(
    [
        1.0 * N4(-np.sqrt(3) / 3, -np.sqrt(3) / 3),
        1.0 * N4(-np.sqrt(3) / 3, np.sqrt(3) / 3),
        1.0 * N4(np.sqrt(3) / 3, -np.sqrt(3) / 3),
        1.0 * N4(np.sqrt(3) / 3, np.sqrt(3) / 3),
    ]
)
print("A1:", A1)
print("A2:", A2)
print("A3:", A3)
print("A4:", A4)

# %%
mesh = gf.Mesh("empty", 2)
mesh.add_convex(
    gf.GeoTrans("GT_QK(2,1)"),
    [[-1.0, 1.0, -1.0, 1.0], [-1.0, -1.0, 1.0, 1.0]],
)
mfu = gf.MeshFem(mesh, 1)
mfd = gf.MeshFem(mesh, 1)
mfu.set_fem(mfu.set_fem(gf.Fem("FEM_PRODUCT(FEM_PK(1, 1), FEM_PK(1, 1))")))
mfd.set_fem(mfu.set_fem(gf.Fem("FEM_PRODUCT(FEM_PK(1, 1), FEM_PK(1, 1))")))
mim = gf.MeshIm(mesh, gf.Integ("IM_PRODUCT(IM_GAUSS1D(3), IM_GAUSS1D(3))"))
A = gf.asm_volumic_source(mim, mfu, mfd, np.array([[1, 1, 1, 1]]))
print("A", A)
