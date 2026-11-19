"""Deliverable 1, task 1.1 figure. Run from anywhere: python deliverable_1/make_figures.py"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
LISTINGS_CSV = HERE.parent / "craigslist.csv"
OUTPUT_DIR = HERE / "output"

COLUMNS = ["price", "year", "manufacturer", "model", "odometer"]
SNAPSHOT_YEAR = 2021  # every listing was posted in April or May 2021
BUDGET = 5000


def load_listings():
    """Load listings, removing reposts and placeholder values."""
    df = pd.read_csv(LISTINGS_CSV, usecols=COLUMNS)
    df = df.dropna(subset=["price", "year", "manufacturer", "model", "odometer"])
    df = df.drop_duplicates(["price", "year", "manufacturer", "model", "odometer"])
    # Prices under $500 and odometers under 100 miles are mostly placeholders ($0, $1, 0 mi).
    return df[(df.price >= 500) & (df.odometer >= 100)]


def budget_figure(df):
    """Task 1.1: with $5,000, what years and mileages can a first-time buyer get?"""
    cars = df[df.price <= BUDGET]
    shown = cars[(cars.year >= 1990) & (cars.year <= SNAPSHOT_YEAR) & (cars.odometer < 300_000)]
    fig, ax = plt.subplots(figsize=(8, 5))
    year_bins = [y - 0.5 for y in range(1990, SNAPSHOT_YEAR + 2)]
    odometer_bins = range(0, 300_001, 10_000)
    *_, cells = ax.hist2d(shown.year, shown.odometer, bins=[year_bins, odometer_bins], cmin=1)
    fig.colorbar(cells, label="Number of listings")
    ax.set_title(f"Used car listings up to ${BUDGET:,}, 2021 (n = {len(shown):,})\n"
                 f"Median listing: {shown.year.median():.0f} model year, "
                 f"{shown.odometer.median():,.0f} miles")
    ax.set_xlabel("Model year")
    ax.set_ylabel("Odometer (miles)")
    ax.yaxis.set_major_formatter("{x:,.0f}")
    fig.tight_layout()
    return fig


def main():
    df = load_listings()
    OUTPUT_DIR.mkdir(exist_ok=True)
    budget_figure(df).savefig(OUTPUT_DIR / "task_1_1_budget.png", dpi=200)
    print(f"Saved figure to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
