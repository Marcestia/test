from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from macro_agent import REGIME_LABELS, MacroLabel


@dataclass
class MacroInsight:
    zone: str
    regime: MacroLabel
    narrative: str
    confidence: str


def _format_change(value: float) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.1f}%"


def interpret_regime(zone: str, regime: MacroLabel, ratios: pd.DataFrame, lookback_days: int = 90) -> MacroInsight:
    """Produit une explication lisible du régime macro courant.

    La fonction reste volontairement simple pour être gratuite et portable.
    Il sera facile de remplacer `narrative` par un appel à un LLM hébergé.
    """

    latest = ratios.iloc[-1]
    pct = ratios.pct_change(periods=lookback_days).iloc[-1] * 100

    narrative_lines = [
        f"Régime détecté : {REGIME_LABELS.get(regime, regime)}.",
        f"Croissance (equity/oil) : niveau {latest['growth_ratio']:.2f} ({_format_change(pct['growth_ratio'])} sur {lookback_days}j).",
        f"Inflation (gold/equity) : niveau {latest['inflation_ratio']:.2f} ({_format_change(pct['inflation_ratio'])} sur {lookback_days}j).",
        f"Protection (gold/bond) : niveau {latest['gold_bond_ratio']:.2f} ({_format_change(pct['gold_bond_ratio'])} sur {lookback_days}j).",
    ]

    guidance = {
        "CROISSANCE_DESINFLATION": "Contexte porteur pour les actifs risqués, surveiller un éventuel retournement inflationniste.",
        "SURCHAUFFE": "Croissance encore solide mais inflation en hausse : privilégier les actifs réels / value et réduire la duration obligataire.",
        "STAGFLATION": "Croissance molle et inflation tenace : favoriser la diversification (or, matières premières) et limiter le bêta actions.",
        "RECESSION": "Croissance faible et inflation en reflux : privilégier la qualité (obligations de bonne signature, secteurs défensifs).",
    }

    narrative_lines.append(guidance.get(regime, ""))

    return MacroInsight(
        zone=zone,
        regime=regime,
        narrative="\n".join(narrative_lines),
        confidence="Heuristique (rolling MA) – remplaçable par un LLM hébergé si disponible.",
    )

