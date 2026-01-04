from __future__ import annotations

from typing import Dict

import pandas as pd

MacroLabel = str

REGIME_LABELS: Dict[str, str] = {
    "CROISSANCE_DESINFLATION": "Croissance + désinflation",
    "SURCHAUFFE": "Croissance + inflation",
    "STAGFLATION": "Croissance en berne + inflation",
    "RECESSION": "Croissance en berne + désinflation",
}


def detect_trend(series: pd.Series, short_window: int = 20, long_window: int = 60) -> bool:
    short = series.rolling(short_window).mean()
    long = series.rolling(long_window).mean()
    return short.iloc[-1] > long.iloc[-1]


def macro_regime(ratios: pd.DataFrame, short_window: int = 20, long_window: int = 60) -> MacroLabel:
    growth_up = detect_trend(ratios["growth_ratio"], short_window=short_window, long_window=long_window)
    inflation_up = detect_trend(
        ratios["inflation_ratio"], short_window=short_window, long_window=long_window
    )

    return classify_regime(growth_up=growth_up, inflation_up=inflation_up)


def classify_regime(growth_up: bool, inflation_up: bool) -> MacroLabel:
    if growth_up and not inflation_up:
        return "CROISSANCE_DESINFLATION"
    if growth_up and inflation_up:
        return "SURCHAUFFE"
    if not growth_up and inflation_up:
        return "STAGFLATION"
    return "RECESSION"


def macro_regime_series(
    ratios: pd.DataFrame, short_window: int = 20, long_window: int = 60
) -> pd.Series:
    """Calcule un régime macro daté pour toute l'historique."""

    growth_short = ratios["growth_ratio"].rolling(short_window).mean()
    growth_long = ratios["growth_ratio"].rolling(long_window).mean()
    inflation_short = ratios["inflation_ratio"].rolling(short_window).mean()
    inflation_long = ratios["inflation_ratio"].rolling(long_window).mean()

    growth_up = growth_short > growth_long
    inflation_up = inflation_short > inflation_long

    regime_series = pd.Series(index=ratios.index, dtype="object")
    regime_series.loc[growth_up & ~inflation_up] = "CROISSANCE_DESINFLATION"
    regime_series.loc[growth_up & inflation_up] = "SURCHAUFFE"
    regime_series.loc[~growth_up & inflation_up] = "STAGFLATION"
    regime_series.loc[~growth_up & ~inflation_up] = "RECESSION"

    return regime_series.dropna()


def regime_changes(regime_series: pd.Series) -> pd.DataFrame:
    """Historise les changements de régime (date + transition)."""

    changes = []
    previous_label: MacroLabel | None = None

    for date, label in regime_series.items():
        if previous_label is None:
            previous_label = label
            continue

        if label != previous_label:
            changes.append({"date": date, "from": previous_label, "to": label})
            previous_label = label

    return pd.DataFrame(changes)
