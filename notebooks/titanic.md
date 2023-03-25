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

# Titanicのデータのダウンロード

Titanicのデータをダウンロードします。

```{code-cell}
!kaggle competitions download -c titanic
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
```
