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
import matplotlib.pyplot as plt

# %% [markdown]
# ## 積分法の定義
#
# 定義するのは積分法 `mim` です．GetFEM にデフォルトの積分法はありません．
# したがって，これは積分法を定義するためには必須です．
# もちろん，積分法の次数は，選択された有限要素法に好都合な積分を行うため，十分に選定しなければなりません．

# %%
im = gf.Integ("IM_GAUSS1D(1)")
print("im")
print(im)
print("im.pts()")
print(im.pts())
print("im.coeffs()")
print(im.coeffs())

# %%
pts = im.pts()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(
    pts[0],
    pts[0] * 0.0 + 0.5,
    linewidth=0,
    marker="o",
    markersize=10,
    markeredgecolor="red",
    markerfacecolor="red",
)
ax.grid()
ax.set_xlim(-0.2, 1.2)
ax.set_xticks([-0.2, 0.0, 0.5, 1.0, 1.2])
ax.set_ylim(-0.2, 1.2)
ax.set_yticks([-0.2, 0.5, 1.2])
plt.show()

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
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(
    pts[0],
    pts[0] * 0.0 + 0.5,
    linewidth=0,
    marker="o",
    markersize=10,
    markeredgecolor="red",
    markerfacecolor="red",
)
ax.grid()
ax.set_xlim(-0.2, 1.2)
ax.set_xticks(
    [
        -0.2,
        0.0,
        0.5 - np.sqrt(1.0 / 3.0) / 2.0,
        0.5 + np.sqrt(1.0 / 3.0) / 2.0,
        1.0,
        1.2,
    ]
)
ax.set_ylim(-0.2, 1.2)
ax.set_yticks([-0.2, 0.5, 1.2])
plt.show()

# %%
im = gf.Integ("IM_GAUSS1D(5)")
print("im")
print(im)
print("im.pts()")
print(im.pts())
print("im.coeffs()")
print(im.coeffs())

# %%
pts = im.pts()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(
    pts[0],
    pts[0] * 0.0 + 0.5,
    linewidth=0,
    marker="o",
    markersize=10,
    markeredgecolor="red",
    markerfacecolor="red",
)
ax.grid()
ax.set_xlim(-0.2, 1.2)
ax.set_xticks(
    [
        -0.2,
        0.0,
        0.5 - np.sqrt(3.0 / 5.0) / 2.0,
        0.5,
        0.5 + np.sqrt(3.0 / 5.0) / 2.0,
        1.0,
        1.2,
    ]
)
ax.set_ylim(-0.2, 1.2)
ax.set_yticks([-0.2, 0.5, 1.2])
plt.show()

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
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(
    pts[0],
    pts[1],
    linewidth=0,
    marker="o",
    markersize=10,
    markeredgecolor="red",
    markerfacecolor="red",
)
ax.grid()
ax.set_xlim(-0.2, 1.2)
ax.set_xticks(
    [
        -0.2,
        0.0,
        0.5 - np.sqrt(1.0 / 3.0) / 2.0,
        0.5 + np.sqrt(1.0 / 3.0) / 2.0,
        1.0,
        1.2,
    ]
)
ax.set_ylim(-0.2, 1.2)
ax.set_yticks(
    [
        -0.2,
        0.0,
        0.5 - np.sqrt(1.0 / 3.0) / 2.0,
        0.5 + np.sqrt(1.0 / 3.0) / 2.0,
        1.0,
        1.2,
    ]
)
plt.show()
