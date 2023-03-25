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
