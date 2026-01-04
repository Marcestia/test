from __future__ import annotations

from typing import Dict, Iterable

import pandas as pd
import yfinance as yf


DEFAULT_PERIOD = "5y"


ASSETS: Dict[str, Dict[str, str]] = {
    "US": {
        "equity": "^GSPC",  # S&P 500
        "bond": "TLT",  # Obligations US long terme
        "gold": "GLD",  # Or
        "oil": "CL=F",  # Pétrole WTI
    },
    "EU": {
        "equity": "^STOXX",
        "bond": "IEI",
        "gold": "GLD",
        "oil": "BZ=F",  # Brent
    },
}


def load_prices(ticker: str, period: str = DEFAULT_PERIOD) -> pd.Series:
    data = yf.download(ticker, period=period, progress=False)

    if data.empty:
        raise ValueError(f"Aucune donnée pour {ticker}")

    if "Adj Close" in data.columns:
        return data["Adj Close"]

    if "Close" in data.columns:
        return data["Close"]

    if isinstance(data.columns, pd.MultiIndex):
        for col in data.columns:
            if "Close" in col:
                return data[col]

    return data.iloc[:, -1]


def load_zone_data(zone: str, period: str = DEFAULT_PERIOD) -> pd.DataFrame:
    assets = ASSETS[zone]
    series = []

    for name, ticker in assets.items():
        s = load_prices(ticker, period=period)
        s.name = name
        series.append(s)

    df = pd.concat(series, axis=1)
    return df.dropna()


def load_zones(zones: Iterable[str], period: str = DEFAULT_PERIOD) -> Dict[str, pd.DataFrame]:
    """Télécharge les séries de plusieurs zones.

    Retourne un dictionnaire {zone: DataFrame} pour permettre
    des comparaisons côte à côte sans hypothèses sur le merge.
    """

    datasets: Dict[str, pd.DataFrame] = {}
    for zone in zones:
        datasets[zone] = load_zone_data(zone, period=period)
    return datasets
