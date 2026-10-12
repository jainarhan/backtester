import pandas as pd

df = pd.read_parquet("reliance.parquet")

# if columns look like ('Close', 'RELIANCE.NS'), flatten them
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

print(df.head())
print(df.info())
print(df.isna().sum())


df["ret"] = df["Close"].pct_change()          # simple return
import numpy as np
df["log_ret"] = np.log(df["Close"] / df["Close"].shift(1))

print(df[["Close", "ret", "log_ret"]].head())
print(df["ret"].describe())

(1 + df["ret"]).cumprod().plot()



import matplotlib.pyplot as plt
(1 + df["ret"]).cumprod().plot()
plt.show()