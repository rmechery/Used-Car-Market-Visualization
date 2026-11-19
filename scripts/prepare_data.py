"""Shrink the raw Kaggle CSVs into small parquet files the dashboard can ship with.

The raw Craigslist CSV is 1.3 GB, too big for GitHub or Streamlit Community Cloud,
so this keeps only the columns and rows the dashboard uses and commits the result
to data/. Re-run it only if the cleaning rules change:

    python scripts/prepare_data.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_LISTINGS = ROOT / "craigslist.csv"
RAW_SPECS = ROOT / "car_features_and_msrp.csv"
OUT = ROOT / "data"

LISTING_COLUMNS = ["price", "year", "manufacturer", "model", "odometer", "condition", "state"]
KEY = ["price", "year", "manufacturer", "model", "odometer"]
CONDITIONS = ["salvage", "fair", "good", "excellent", "like new", "new"]
SPEC_COLUMNS = {"Engine HP": "hp", "highway MPG": "highway_mpg", "city mpg": "city_mpg", "MSRP": "msrp"}


def prepare_listings():
    """Drop reposts and placeholder values ($0 prices, 0-mile odometers)."""
    df = pd.read_csv(RAW_LISTINGS, usecols=LISTING_COLUMNS)
    df = df.dropna(subset=KEY).drop_duplicates(KEY)
    df = df[(df.price >= 500) & (df.price <= 250_000) & (df.odometer >= 100) & (df.odometer <= 500_000)]
    df = df.assign(
        price=df.price.astype("int32"),
        year=df.year.astype("int16"),
        odometer=df.odometer.astype("int32"),
        manufacturer=df.manufacturer.astype("category"),
        model=df.model.str.strip().str.lower().astype("category"),
        condition=pd.Categorical(df.condition, categories=CONDITIONS, ordered=True),
        state=df.state.astype("category"),
    )
    return df.reset_index(drop=True)


def prepare_specs():
    """One row per make, model, and model year: median specs and MSRP across trims."""
    specs = pd.read_csv(RAW_SPECS)
    specs = specs.rename(columns=SPEC_COLUMNS)
    specs["make"] = specs.Make
    specs["manufacturer"] = specs.Make.str.lower()
    specs["model"] = specs.Model.str.lower()
    specs["model_name"] = specs.Model
    specs["year"] = specs.Year.astype("int16")
    keys = ["manufacturer", "model", "make", "model_name", "year"]
    return specs.groupby(keys, as_index=False)[list(SPEC_COLUMNS.values())].median()


def main():
    OUT.mkdir(exist_ok=True)
    listings = prepare_listings()
    listings.to_parquet(OUT / "listings.parquet", index=False, compression="zstd")
    specs = prepare_specs()
    specs.to_parquet(OUT / "specs.parquet", index=False, compression="zstd")
    print(f"listings: {len(listings):,} rows, specs: {len(specs):,} rows -> {OUT}")


if __name__ == "__main__":
    main()
