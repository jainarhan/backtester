import yfinance as yf
import pandas as pd
import os

tickers = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BEL", "BHARTIARTL",
    "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "ETERNAL",
    "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO",
    "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK", "INFY",
    "ITC", "JIOFIN", "JSWSTEEL", "KOTAKBANK", "LT",
    "M&M", "MARUTI", "NESTLEIND", "NTPC", "ONGC",
    "POWERGRID", "RELIANCE", "SBILIFE", "SBIN", "SHRIRAMFIN",
    "SUNPHARMA", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TCS",
    "TECHM", "TITAN", "TRENT", "ULTRACEMCO", "WIPRO",
]
tickers = [t + ".NS" for t in tickers]

raw = yf.download(tickers, start="2015-01-01", auto_adjust=True, progress=True)

close = raw["Close"]
volume = raw["Volume"]

# see which tickers failed or have little data
print("\nRows per ticker (non-null):")
print(close.count().sort_values().head(10))
print("\nTickers with no data:", list(close.columns[close.isna().all()]))

os.makedirs("data", exist_ok=True)
close.to_parquet("data/close.parquet")
volume.to_parquet("data/volume.parquet")
print("\nSaved. Shape:", close.shape)