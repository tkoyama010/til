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
# https://github.com/matplotlib/matplotlib/issues/5836#issuecomment-179592427
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import matplotlib.pyplot as plt

# %% [code]
# https://github.com/matplotlib/matplotlib/issues/5836#issuecomment-179592427
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import matplotlib.pyplot as plt

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
