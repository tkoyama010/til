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
#
# # Modal Assurance Criterion
#
# この記事では、MAC(Modal Assurance Criterion)の使い方をレビューします。
# MACは、2組のベクトル $\left\{\varphi _A\right\}$ と $\left\{\varphi _X\right\}$ の大きな差に最も敏感で、モード形状の小さな差には比較的鈍感な統計的指標です。
# 得られたスカラーはMAC行列に配置します。
#
# $$
# MAC\left(A,X\right)=\frac{\left|\sum _{j=1}^n\left\{\varphi _A\right\}_j^{ }\left\{\varphi _X\right\}_j\right|^2}{\left(\sum _{j=1}^n\left\{\varphi _A\right\}_j^{ }\left\{\varphi _A\right\}_j^{ }\right)\left(\sum _{j=1}^n\left\{\varphi _X\right\}_j^{ }\left\{\varphi _X\right\}_j^{ }\right)}.
# $$

# %% [markdown]
#
# 例として以下のような剛性行列$A$を定義して固有値と固有ベクトルを計算します。
# 簡単のため質量行列は単位行列とします。

# %%
import numpy as np

A = np.array([[1.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 2.0]])

# %% [markdown]
#
# 剛性行列の固有振動数と固有ベクトルは以下のとおりです。

# %%
eigenvalues, eigenvectors = np.linalg.eigh(A)
omega_a = (1 / (2 * np.pi)) * np.sqrt(eigenvalues)
phi_a = eigenvectors

# %% [markdown]
#
# 剛性行列$A$同士のMACを計算してみます。

# %%
MAC = (phi_a.T @ phi_a) ** 2 / ((phi_a.T @ phi_a) * (phi_a.T @ phi_a))
print(MAC)
