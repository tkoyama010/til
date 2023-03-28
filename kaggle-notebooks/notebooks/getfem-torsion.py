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
# # GetFEMの動作確認
#
#
# 半径方向の単位ベクトル $P$ は以下の式であらわされる。
#
# ```math
# P＝\begin{pmatrix}\cos \theta &\sin \theta \end{pmatrix}
# ```
#
# ベクトル $P$ を角度 $\theta$ で微分すると接線方向の単位ベクトルを得ることができる。
#
# ```math
# \frac{dP}{d\theta }=\begin{pmatrix}-\sin \theta &\cos \theta \end{pmatrix}
# ```
#
# このノートはGetFEMの動作確認を行うために作成したものです。

# %%
import getfem as gf
