import pandas as pd


def compute_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule les ratios macro sur une zone donnée.

    Le résultat est un DataFrame aligné sur les dates d'entrée.
    """

    expected_cols = {"equity", "oil", "gold", "bond"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise KeyError(f"Colonnes manquantes pour calculer les ratios: {missing}")

    ratios = pd.DataFrame(
        {
            "growth_ratio": df["equity"] / df["oil"],
            "inflation_ratio": df["gold"] / df["equity"],
            "gold_bond_ratio": df["gold"] / df["bond"],
        }
    )

    return ratios.dropna()
