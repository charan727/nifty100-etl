import pandas as pd
from pathlib import Path

from src.screener.engine import ScreenerEngine


engine = ScreenerEngine()

presets = [
    "quality_compounder",
    "value_pick",
    "growth_accelerator",
    "dividend_champion",
    "debt_free_bluechip",
    "turnaround_watch"
]

output_file = (
    Path(__file__).resolve().parents[2]
    / "output"
    / "screener_output.xlsx"
)

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    for preset in presets:

        print(f"Generating sheet : {preset}")

        df = engine.apply_filters(preset)

        df.to_excel(
            writer,
            sheet_name=preset[:31],
            index=False
        )

print("\n===================================")
print("screener_output.xlsx Generated")
print("Location :", output_file)
print("===================================")