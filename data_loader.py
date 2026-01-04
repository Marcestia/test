import yfinance as yf
import pandas as pd

ASSETS = {
    "US": {
        "equity": "^GSPC",      # S&P 500
        "bond": "TLT",          # Obligations US long terme
        "gold": "GLD",          # Or
        "oil": "CL=F"           # Pétrole WTI
    },
    "EU": {
        "equity": "^STOXX",
        "bond": "IEI",
        "gold": "GLD",
        "oil": "BZ=F"           # Brent
    }
}

def load_prices(ticker, period="2y"):
    data = yf.download(ticker, period=period, progress=False)

    if data.empty:
        raise ValueError(f"Aucune donnée pour {ticker}")

    # 1️⃣ Cas colonnes simples
    if "Adj Close" in data.columns:
        return data["Adj Close"]

    if "Close" in data.columns:
        return data["Close"]

    # 2️⃣ Cas colonnes multi-index
    if isinstance(data.columns, pd.MultiIndex):
        # On cherche une colonne contenant 'Close'
        for col in data.columns:
            if "Close" in col:
                return data[col]

    # 3️⃣ Fallback ultime (dernière colonne)
    return data.iloc[:, -1]



def load_zone_data(zone):
    assets = ASSETS[zone]
    series = []

    for name, ticker in assets.items():
        s = load_prices(ticker)
        s.name = name
        series.append(s)

    # Alignement temporel propre
    df = pd.concat(series, axis=1)

    # Nettoyage (jours communs uniquement)
    df = df.dropna()

    return df

