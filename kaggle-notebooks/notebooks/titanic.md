---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst,ipynb
  main_language: python
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
---

# タイタニック号 災害から学ぶ機械学習

## データの取得

Titanicのデータを取得します。

```{code-cell}
!kaggle competitions download -c titanic --quiet
```

ダウンロードの際には`kaggle.json`ファイルを `~/.kaggle/kaggle.json` に配置しておく必要があります。
`titanic.zip`ファイルがダウンロードされますのでカレントディレクトリに展開します。

```{code-cell}
!unzip titanic.zip
```

`train.csv` ファイルに訓練用のデータが保存されていますので `polars.read_csv` で読み込みます。

```{code-cell}
import polars as pl
train = pl.read_csv("train.csv")
train.head(3)
```

`test.csv` ファイルにテスト用のデータが保存されていますので同様に `polars.read_csv` で読み込みます。

```{code-cell}
import polars as pl
test = pl.read_csv("test.csv")
test.head(3)
```
