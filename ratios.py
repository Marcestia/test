import pandas as pd


def compute_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule les ratios macro sur une zone donnée.

    Le résultat est un DataFrame aligné sur les dates d'entrée.
    """

    ratios = pd.DataFrame(
        {
            "growth_ratio": df["equity"] / df["oil"],
            "inflation_ratio": df["gold"] / df["equity"],
            "gold_bond_ratio": df["gold"] / df["bond"],
        }
    )

    return ratios.dropna()
