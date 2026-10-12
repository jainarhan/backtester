def momentum(close, lookback=252, skip=21):
    # return from (lookback) days ago to (skip) days ago
    return close.shift(skip) / close.shift(lookback) - 1

def reversal(close, lookback=5):
    # stocks that fell recently are expected to bounce, so flip the sign
    return -close.pct_change(lookback)

def low_vol(close, lookback=60):
    # calmer stocks score higher, so flip the sign of volatility
    return -close.pct_change().rolling(lookback).std()