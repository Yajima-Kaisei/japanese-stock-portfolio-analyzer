import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import matplotlib
matplotlib.rcParams['font.family'] = 'MS Gothic'
import streamlit as st

# データ取得
ticker_df = pd.read_excel("ticker_code.xlsx")
ticker_df["コード"] = ticker_df["コード"].astype(str)  # ② 文字列化
ticker_dict = dict(zip(ticker_df["銘柄名"], ticker_df["コード"] + ".T"))
name_dict = {v: k for k, v in ticker_dict.items()}

names = st.multiselect(
    "銘柄を選択",
    options=list(ticker_dict.keys()),
    default=["ＳＢ", "ＫＤＤＩ", "トヨタ"]
)

if len(names) == 0:
    st.warning("銘柄を1つ以上選んでください")
    st.stop()

tickers = [ticker_dict[name] for name in names]

df = yf.download(tickers, start="2019-01-01", end="2026-05-01")

if df.empty:
    st.error("株価データが取得できませんでした")
    st.stop()

df = df["Close"]

if len(tickers) == 1:
    df = df.to_frame()

df = df.pct_change().dropna()

# 平均・分散・共分散
Rp = df.mean() * 250
Var_Rp = df.var() * 250

# モンテカルロシミュレーション
rf = st.number_input(
    "無リスク金利",
    value=0.03157
)
num_simulations = 10000
E_Rp = []
Sigma_Rp = []
S_ratio = []
weights_record = []

for i in range(num_simulations):
    weights = np.random.random(len(tickers))
    weights = weights / weights.sum()
    e_rp = np.dot(weights, Rp)
    port_variance = np.dot(weights, np.dot(df.cov() * 250, weights))
    sigma = np.sqrt(port_variance)
    s_r = (e_rp - rf) / sigma
    E_Rp.append(e_rp)
    Sigma_Rp.append(sigma)
    S_ratio.append(s_r)
    weights_record.append(weights)


# 最適ポートフォリオ
max_idx = np.argmax(S_ratio)
best_weights = weights_record[max_idx]
opt_risk = Sigma_Rp[max_idx]
opt_return = E_Rp[max_idx]
max_sr = S_ratio[max_idx]

# CML
Risk_range = np.linspace(
    min(Sigma_Rp),
    max(Sigma_Rp),
    100
)
CML_return = [rf + max_sr * x for x in Risk_range]

# 可視化
st.title("ポートフォリオ分析アプリ")
plt.figure(figsize=(10, 6))
plt.scatter(Sigma_Rp, E_Rp, c=S_ratio, cmap='viridis', alpha=0.5)
plt.colorbar(label="シャープレシオ")
plt.plot(Risk_range, CML_return, color='red', label='資本市場線(CML)')
plt.plot(opt_risk, opt_return, "ro", markersize=12, label='最適ポートフォリオ')
plt.xlabel("リスク")
plt.ylabel("期待リターン")
plt.title(f"{','.join(names)} 効率的フロンティア")
plt.xlim(min(Sigma_Rp)-0.01, max(Sigma_Rp)+0.01)
plt.ylim(min(E_Rp)-0.01, max(E_Rp)+0.01)
plt.legend()
st.pyplot(plt)
st.subheader("最適ポートフォリオ")

st.write(f"期待リターン: {opt_return:.2%}")

st.write(f"リスク: {opt_risk:.2%}")

st.write(f"シャープレシオ: {max_sr:.2f}")
st.subheader("最適ウェイト")

for ticker, weight in zip(tickers, best_weights):
    name = name_dict.get(ticker, ticker)  # 保険付き
    st.write(f"{name}: {weight:.2%}")

# =========================
# 100万円投資シミュレーション
# =========================

investment = 1_000_000

# 各銘柄への投資額
allocation = best_weights * investment

st.subheader("投資配分（100万円）")

for ticker, amount in zip(tickers, allocation):
    name = name_dict.get(ticker, ticker)
    st.write(f"{name}: ¥{amount:,.0f}")

# =========================
# 期待リターンで将来価値
# =========================

st.subheader("1年後予測（期待値ベース）")

future_value = investment * (1 + opt_return)
profit = future_value - investment

st.write(f"期待資産額: ¥{future_value:,.0f}")
st.write(f"期待利益: ¥{profit:,.0f}")

# =========================
# 銘柄ごとの利益
# =========================

st.subheader("銘柄別の期待利益")

individual_returns = Rp.values  # 各銘柄の年リターン

for ticker, invest, r in zip(tickers, allocation, individual_returns):
    name = name_dict.get(ticker, ticker)

    future = invest * (1 + r)
    gain = future - invest

    st.write(f"{name}: 投資 ¥{invest:,.0f} → 利益 ¥{gain:,.0f}")