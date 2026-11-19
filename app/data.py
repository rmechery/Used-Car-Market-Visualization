"""Cached loaders for the preprocessed data in data/ (built by scripts/prepare_data.py)."""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data"
SNAPSHOT_YEAR = 2021  # every listing was posted in April or May 2021
CONDITIONS = ["salvage", "fair", "good", "excellent", "like new", "new"]

# Shared chart colors: neutral for the market, one accent for "your car".
GRAY = "#b0b0b0"
ACCENT = "#c0392b"
BLUE = "#2c5aa0"


@st.cache_data
def load_listings():
    return pd.read_parquet(DATA / "listings.parquet")


@st.cache_data
def load_specs():
    return pd.read_parquet(DATA / "specs.parquet")


@st.cache_data
def load_matched_listings():
    """Listings whose make and model exactly match the specs data, with display names.

    Exact name match only: listings with a trim in the model name ("civic lx") are left out.
    """
    names = load_specs()[["manufacturer", "model", "make", "model_name"]].drop_duplicates(["manufacturer", "model"])
    listings = load_listings().astype({"manufacturer": str, "model": str})
    matched = listings.merge(names, on=["manufacturer", "model"])
    matched["car"] = matched.make + " " + matched.model_name
    return matched
