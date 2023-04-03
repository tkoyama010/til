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
# # タイタニック号 災害から学ぶ機械学習
#
# ## データの取得
#
# Titanicのデータを取得します。

# %%
# !kaggle competitions download -c titanic --quiet

# %% [markdown]
# ダウンロードの際には`kaggle.json`ファイルを `~/.kaggle/kaggle.json` に配置しておく必要があります。
# `titanic.zip`ファイルがダウンロードされますのでカレントディレクトリに展開します。

# %%
# !unzip titanic.zip

# %% [markdown]
# `train.csv` ファイルに訓練用のデータが保存されていますので `pandas.read_csv` で読み込みます。

# %%
import pandas as pd

train = pd.read_csv("train.csv")
train.head(3)

# %% [markdown]
# `test.csv` ファイルにテスト用のデータが保存されていますので同様に `pandas.read_csv` で読み込みます。

# %%
import pandas as pd

test = pd.read_csv("test.csv")
test.head(3)
