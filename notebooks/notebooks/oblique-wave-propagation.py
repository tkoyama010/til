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
# # 水平成層地盤を対象とした平面波斜め入射時の時刻歴応答解析の定式化と検証

# %% [markdown]
# ## はじめに
#
# 水平成層地盤の時刻歴応答解析では，大きなせん断ひずみによる非線形特性を取り入れた検討が可能であり，一般的に S 波の鉛直入射を仮定した解析が行われている。
# これに対し，SV 波が斜め入射したときの解析は振動数領域では実施されているものの，時刻歴応答解析での事例はあまり見られない。
# 平面波斜め入射時の水平成層地盤の時刻歴応答解析の定式化は，将来 3 次元地盤構造を対象とした平面波斜め入射時の時刻歴応答解析を実施する際の境界条件としても必要となる。
# 本稿では平面波斜め入射時の水平成層地盤の時刻歴応答解析法について，振動数領域での表現をベースに定式化を行い，その妥当性を検討した。
# 本稿では SV 波のみを示すが，SH 波斜め入射による 2 次元面内問題も同様に誘導することができる。

# %% [markdown]
# ## 検証解析
#
# 前節の定式化を元に平面波の斜め面内波入射解析を行い，一般化 RT 法による解析結果との比較を行った。
# 

# %% [code]
print("Hello world!")
