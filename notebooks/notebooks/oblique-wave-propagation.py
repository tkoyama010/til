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
# ## 水平成層地盤の斜め入射時の面内波振動方程式
#
# 最初に斜め入射時に現れる空間微分を時間微分に変換する。
# 斜め入射角を $\theta _S$，入射角のS波速度を $V_{SN}$ とすると，水平方向の apparent velocity が $C=\dfrac{V_{SN}}{\sin \theta _S}$ で表現される。
# このとき水平方向 $x$ に伝播する波動場は $U\left(t-\dfrac{x}{C},z\right)$ で表されることから， $x$ に関する偏微分項は次式で表現される。
# $$
# \dfrac{dU}{\ dx}=-\dfrac{1}{C}\dfrac{dU}{dt}
# $$
# $$
# \dfrac{d^2U}{\ dx^2}=\dfrac{1}{C^2}\dfrac{d^2U}{dt^2}
# $$
# 面内波の支配方程式を深さ方向($𝑧$方向)に離散化し，時間領域での薄層法の表現を得る。
# ここで， $𝑥$ の微分項に上式を適用すると次式が得られる。
# $$
# -\dfrac{1}{C^2}\begin{bmatrix}A_P&\\&A_S\end{bmatrix}\dfrac{\partial ^2}{\partial t^2}\begin{Bmatrix}U_x\\U_z\end{Bmatrix}-\dfrac{1}{C}\begin{bmatrix}&B^T\\-B&\end{bmatrix}\dfrac{\partial }{\partial t}\begin{Bmatrix}U_x\\U_z\end{Bmatrix}+\begin{bmatrix}G_S&\\&G_P\end{bmatrix}\begin{Bmatrix}U_x\\U_z\end{Bmatrix}+\begin{bmatrix}M&\\&M\end{bmatrix}\dfrac{\partial ^2}{\partial t^2}\begin{Bmatrix}U_x\\U_z\end{Bmatrix}+\begin{Bmatrix}F_x\\F_z\end{Bmatrix}=\begin{Bmatrix}0\\0\end{Bmatrix}
# $$
# 各変数の定義は {cite:ts}`Kausel1981StiffnessMF` を参照のこと。
# $𝐹_𝑥$ , $𝐹_𝑧$ はモデル底面位置 $𝑁$ のみに応力 $𝐹_𝑥$ ,  $𝐹_𝑧$ が作用し，それ以外は $0$ となる。

# %% [markdown]
# ## 検証解析
#
# 前節の定式化を元に平面波の斜め面内波入射解析を行い，一般化 RT 法による解析結果との比較を行った。
#

# %% [code]
print("Hello world!")
