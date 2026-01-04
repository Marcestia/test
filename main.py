from data_loader import load_zone_data
from ratios import compute_ratios
from macro_agent import macro_regime

ZONE = "US"  # change ici : US / EU

data = load_zone_data(ZONE)
print(data.head())
print(data.columns)

ratios = compute_ratios(data)

regime = macro_regime(ratios)

print(f"Zone : {ZONE}")
print(f"Régime macro actuel : {regime}")
