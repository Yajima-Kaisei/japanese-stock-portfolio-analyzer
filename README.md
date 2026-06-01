# Japanese Stock Portfolio Analyzer

## Overview

ゼミで学習したポートフォリオ理論への理解を深めるため、日本株の実データを用いたポートフォリオ分析アプリを開発しました。

本アプリでは、ユーザーが複数の銘柄を選択し、モンテカルロシミュレーションを用いて効率的フロンティアを描画します。また、シャープレシオを基準として最適ポートフォリオを算出し、100万円を投資した場合の資産配分や期待利益を可視化できます。

現在も継続的に改善を進めているプロジェクトであり、分析精度の向上や機能追加に取り組んでいます。


## Features

- 日本株データの取得（Yahoo Finance）
- 効率的フロンティアの可視化
- シャープレシオ最大化による最適ポートフォリオ算出
- 投資配分シミュレーション
- 将来利益の試算
- StreamlitによるWebアプリ化


## Development Environment

- Python 3.12
- Visual Studio Code
- Git
- GitHub
- Streamlit
- Pandas
- NumPy
- Matplotlib
- yfinance
- openpyxl

### Virtual Environment

本プロジェクトは Python 3.12 の仮想環境（venv）上で開発および動作確認を行っています。


## Installation

bash
pip install -r requirements.txt



## Run

bash
streamlit run stock_analysis.py

## Future Improvements

- リスク指標（VaR、CVaR等）の追加
- バックテスト機能の実装
- ポートフォリオ比較機能の追加
- UI/UXの改善
- クラウド環境へのデプロイ
- 分析対象銘柄の拡充

## Purpose

ゼミで学習したポートフォリオ理論が実際の投資に使えるのか興味を持ち、「実際にどの程度の利益が期待できるのか」「どのようなリスクが存在するのか」を自分で分析してみたいと考え、本プロジェクトを開発しました。

単に株価の推移を見るだけでなく、複数銘柄を組み合わせた際のリスクとリターンの関係を可視化し、分散投資による効果や最適な資産配分について検証しています。

本プロジェクトを通じて、Pythonによるデータ分析、統計処理、可視化、およびWebアプリケーション開発のスキル向上に取り組んでいます。

## Notes

本プロジェクトは大学ゼミで学習したポートフォリオ理論の分析コードを基礎とし、個人でWebアプリ化および機能拡張を行ったものです。
