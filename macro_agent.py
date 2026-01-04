def detect_trend(series, window=60):
    short = series.rolling(20).mean()
    long = series.rolling(window).mean()
    return short.iloc[-1] > long.iloc[-1]


def macro_regime(ratios):
    growth_up = detect_trend(ratios["growth_ratio"])
    inflation_up = detect_trend(ratios["inflation_ratio"])

    if growth_up and not inflation_up:
        return "CROISSANCE_DESINFLATION"
    if growth_up and inflation_up:
        return "SURCHAUFFE"
    if not growth_up and inflation_up:
        return "STAGFLATION"
    return "RECESSION"
