"""Task 1.3: compare a few models on price, age, mileage, and specs."""
import streamlit as st

from app.data import SNAPSHOT_YEAR, load_matched_listings, load_specs

MIN_LISTINGS = 100
SPECS = {"hp": "Horsepower", "highway_mpg": "Highway MPG", "city_mpg": "City MPG"}


@st.cache_data
def load_model_summary():
    """One row per model: median listing values joined to median specs across model years."""
    listings = load_matched_listings()
    listings = listings.assign(age=SNAPSHOT_YEAR - listings.year)
    specs = load_specs().groupby(["manufacturer", "model"], as_index=False)[list(SPECS)].median()
    summary = (
        listings.merge(specs, on=["manufacturer", "model"])
        .groupby("car")
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
st.caption("Task 1.3 · first-time buyer")
pick_models, pick_attribute = st.columns([3, 1])
defaults = [car for car in ["Honda Civic", "Hyundai Elantra", "Toyota Corolla"] if car in summary.index]
selected = pick_models.multiselect("Models to compare", summary.index, default=defaults, max_selections=5)
attribute = pick_attribute.selectbox("Attribute to chart", summary.columns.drop("Listings"))
if not selected:
    st.info("Pick at least one model.")
    st.stop()
compared = summary.loc[selected].round().astype(int)

st.write(f"**Median {attribute}**")
st.bar_chart(compared[attribute], horizontal=True, x_label="", y_label="", height=300)

st.dataframe(compared)
st.caption("Listing values are medians from Craigslist, 2021. Specs are medians across model years 1990-2017.")
