from __future__ import annotations

import pandas as pd

from alerts import build_alerts
from data_loader import load_zones
from llm_agent import interpret_regime
from macro_agent import macro_regime_series, regime_changes
from ratios import compute_ratios

ZONES = ["US", "EU"]


def display_zone_snapshot(zone: str, ratios: pd.DataFrame) -> None:
    regimes = macro_regime_series(ratios)
    current_regime = regimes.iloc[-1]
    insight = interpret_regime(zone, current_regime, ratios)
    changes = regime_changes(regimes)
    alerts = build_alerts(zone, changes.tail(3))

    print("=" * 60)
    print(f"Zone : {zone}")
    print(f"Régime macro actuel : {current_regime}")
    print("Narratif synthétique :")
    print(insight.narrative)

    if not changes.empty:
        print("\nDerniers changements de cadran :")
        print(changes.tail(3).to_string(index=False))

    if alerts:
        print("\nAlertes :")
        for alert in alerts:
            print(f"- {alert.render()}")


def main() -> None:
    all_data = load_zones(ZONES)

    last_regimes = {}

    for zone, prices in all_data.items():
        try:
            ratios = compute_ratios(prices)
            regimes = macro_regime_series(ratios)
        except Exception as exc:  # pragma: no cover - CLI resilience
            print(f"[{zone}] Erreur lors du calcul: {exc}")
            continue

        last_regimes[zone] = regimes.iloc[-1]
        display_zone_snapshot(zone, ratios)

    print("\nComparaison inter-zones (régime courant) :")
    comparison_df = pd.DataFrame([last_regimes])
    print(comparison_df.to_string(index=False))


if __name__ == "__main__":
    main()
