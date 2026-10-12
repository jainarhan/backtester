import numpy as np

def summary(pnl):
    pnl = pnl.loc[pnl.ne(0).idxmax():]          # start from first real trade
    ann_ret = pnl.mean() * 252
    ann_vol = pnl.std() * np.sqrt(252)
    equity = (1 + pnl).cumprod()
    drawdown = equity / equity.cummax() - 1
    return {
        "Annual return": f"{ann_ret:.1%}",
        "Annual vol": f"{ann_vol:.1%}",
        "Sharpe": f"{ann_ret / ann_vol:.2f}",
        "Max drawdown": f"{drawdown.min():.1%}",
    }

def rank_ic(signal, close, horizon=1):
    # return from today's close to the close `horizon` days later
    fwd = close.shift(-horizon) / close - 1
    # rank stocks each day, then correlate the two rank tables day by day
    ic = signal.rank(axis=1).corrwith(fwd.rank(axis=1), axis=1)
    return ic.dropna()

def ic_summary(signal, close, horizon=1):
    ic = rank_ic(signal, close, horizon)
    return {
        "Mean IC": f"{ic.mean():.4f}",
        "ICIR": f"{ic.mean() / ic.std():.2f}",
        "% days IC > 0": f"{(ic > 0).mean():.1%}",
    }