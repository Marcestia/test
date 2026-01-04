from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass(frozen=True)
class Alert:
    zone: str
    date: pd.Timestamp
    previous: str
    current: str

    def render(self) -> str:
        return (
            f"[{self.date.date()}] {self.zone}: changement de régime "
            f"{self.previous} -> {self.current}"
        )


def build_alerts(zone: str, regime_change_df: pd.DataFrame) -> List[Alert]:
    alerts: List[Alert] = []
    for _, row in regime_change_df.iterrows():
        alerts.append(Alert(zone=zone, date=row["date"], previous=row["from"], current=row["to"]))
    return alerts
