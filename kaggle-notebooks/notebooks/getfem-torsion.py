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

# %%
import getfem as gf
