import pandas as pd
import matplotlib.pyplot as plt
from signals import momentum, reversal, low_vol
from backtest import run_backtest
from metrics import summary, ic_summary, rank_ic

close = pd.read_parquet("data/close.parquet").dropna(axis=1, how="all")

# name: (signal, rebalance every N days)
tests = {
    "momentum":  (momentum(close), 21),
    "reversal_1d":  (reversal(close), 1),
    "reversal_3d":  (reversal(close), 3),
    "reversal_5d":  (reversal(close), 5),
    "reversal_10d": (reversal(close), 10),
}

rows, curves = {}, {}
for name, (sig, reb) in tests.items():
    gross, net, turnover = run_backtest(close, sig, cost_bps=5, rebalance=reb)
    s_g, s_n = summary(gross), summary(net)
    rows[name] = {
        "Sharpe (gross)": s_g["Sharpe"],
        "Sharpe (net)": s_n["Sharpe"],
        "Ann. return (net)": s_n["Annual return"],
        "Max drawdown": s_n["Max drawdown"],
        "Turnover/day": f"{turnover.mean():.1%}",
    }
    curves[name] = (1 + net).cumprod()

print(pd.DataFrame(rows).T.to_string())



print("\nIC at 1-day horizon:")
print(pd.DataFrame({n: ic_summary(s, close) for n, (s, _) in tests.items()}).T.to_string())

print("\nSignal decay (mean IC by horizon):")
decay = {n: {f"{h}d": rank_ic(s, close, h).mean() for h in [1, 2, 5, 10, 21]}
         for n, (s, _) in tests.items()}
print(pd.DataFrame(decay).T.round(4).to_string())


pd.DataFrame(curves).plot(figsize=(10, 5), title="Growth of ₹1 (net of 5 bps costs)")
plt.show()