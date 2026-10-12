def make_weights(signal):
    ranks = signal.rank(axis=1, pct=True)               # rank stocks within each day (0 to 1)
    w = ranks.sub(ranks.mean(axis=1), axis=0)           # demean: longs and shorts balance out
    w = w.div(w.abs().sum(axis=1), axis=0)              # scale so total exposure = 1
    return w.fillna(0)                                  # no signal -> no position

def run_backtest(close, signal, cost_bps=5, rebalance=21):
    rets = close.pct_change()
    w = make_weights(signal)
    if rebalance > 1:
        w = w.iloc[::rebalance].reindex(w.index).ffill()

    gross = (w.shift(1) * rets).sum(axis=1)
    turnover = w.diff().abs().sum(axis=1)
    net = gross - turnover * cost_bps / 10000
    return gross, net, turnover
