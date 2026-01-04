def compute_ratios(df):
    ratios = {}

    # Proxy croissance
    ratios["growth_ratio"] = df["equity"] / df["oil"]

    # Proxy inflation
    ratios["inflation_ratio"] = df["gold"] / df["equity"]

    # Protection monétaire
    ratios["gold_bond_ratio"] = df["gold"] / df["bond"]

    return ratios
