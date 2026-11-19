"""Deliverable 1, task 1.3 (compare models): streamlit run deliverable_1/app.py"""
import pandas as pd
import streamlit as st

from make_figures import HERE, SNAPSHOT_YEAR, load_listings

SPECS_CSV = HERE.parent / "car_features_and_msrp.csv"
MIN_LISTINGS = 100
SPECS = {"Engine HP": "Horsepower", "highway MPG": "Highway MPG", "city mpg": "City MPG"}


@st.cache_data
def load_model_summary():
    """One row per model: median listing values joined to median specs by make and model name."""
    listings = load_listings()
    listings = listings.assign(age=SNAPSHOT_YEAR - listings.year)

    specs = pd.read_csv(SPECS_CSV)
    specs["manufacturer"] = specs.Make.str.lower()
    specs["model"] = specs.Model.str.lower()
    specs["Car"] = specs.Make + " " + specs.Model
    specs = specs.groupby(["manufacturer", "model", "Car"], as_index=False)[list(SPECS)].median()

    # Exact name match only: listings with a trim in the name ("civic lx") are left out.
    summary = (
        listings.merge(specs, on=["manufacturer", "model"])
        .groupby("Car")
        .agg(
            Listings=("price", "size"),
            Price=("price", "median"),
            Age=("age", "median"),
            Mileage=("odometer", "median"),
            **{label: (column, "first") for column, label in SPECS.items()},
        )
    )
    summary = summary[summary.Listings >= MIN_LISTINGS]
    return summary.rename(columns={"Price": "Price ($)", "Age": "Age (years)", "Mileage": "Mileage (miles)"})


summary = load_model_summary()

st.title("Compare used car models")
pick_models, pick_attribute = st.columns([3, 1])
selected = pick_models.multiselect(
    "Models to compare",
    summary.index,
    default=["Honda Civic", "Hyundai Elantra", "Toyota Corolla"],
    max_selections=5,
)
attribute = pick_attribute.selectbox("Attribute to chart", summary.columns.drop("Listings"))
if not selected:
    st.info("Pick at least one model.")
    st.stop()
compared = summary.loc[selected].round().astype(int)

st.write(f"**Median {attribute}**")
st.bar_chart(compared[attribute], horizontal=True, x_label="", y_label="", height=300)

st.dataframe(compared)
st.caption("Listing values are medians from Craigslist, 2021. Specs are medians across model years 1990-2017.")
