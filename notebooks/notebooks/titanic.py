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

# %% [markdown]
# また、 `seaborn` というライブラリを使用してもデータを取得することができます。

# %%
# see https://seaborn.pydata.org/examples/logistic_regression.html
import seaborn as sns

sns.set_theme(style="darkgrid")

# Load the example Titanic dataset
# df = sns.load_dataset("titanic")
df = train

# Make a custom palette with gendered colors
pal = dict(male="#6495ED", female="#F08080")

# Show the survival probability as a function of age and sex
g = sns.lmplot(
    x="age",
    y="survived",
    col="sex",
    hue="sex",
    data=df,
    palette=pal,
    y_jitter=0.02,
    logistic=True,
    truncate=False,
)
g.set(xlim=(0, 80), ylim=(-0.05, 1.05))
