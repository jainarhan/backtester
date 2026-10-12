import yfinance as yf

df = yf.download("RELIANCE.NS", start="2024-01-01", auto_adjust=True)
df.to_parquet("reliance.parquet")
print("Saved data to reliance.parquet")
print(df.tail())
print(df.shape)