"""Task 1.1: with a given budget, what model years and mileages can a first-time buyer get?"""
import matplotlib.pyplot as plt
import streamlit as st

from app.data import SNAPSHOT_YEAR, load_listings

st.title("Find a car within budget")
st.caption("Task 1.1 · first-time buyer")

listings = load_listings()
left, right = st.columns([2, 1])
budget = left.slider("Budget ($)", 1_000, 30_000, 5_000, step=500, format="$%d")
states = right.multiselect("States (optional)", sorted(listings.state.cat.categories.str.upper()))

cars = listings[listings.price <= budget]
if states:
    cars = cars[cars.state.str.upper().isin(states)]
shown = cars[(cars.year >= 1990) & (cars.year <= SNAPSHOT_YEAR) & (cars.odometer < 300_000)]
if shown.empty:
    st.info("No listings match. Try a larger budget or more states.")
    st.stop()

a, b, c = st.columns(3)
a.metric("Listings in budget", f"{len(shown):,}")
b.metric("Median model year", f"{shown.year.median():.0f}")
c.metric("Median mileage", f"{shown.odometer.median():,.0f} mi")

fig, ax = plt.subplots(figsize=(8, 5))
year_bins = [y - 0.5 for y in range(1990, SNAPSHOT_YEAR + 2)]
odometer_bins = range(0, 300_001, 10_000)
*_, cells = ax.hist2d(shown.year, shown.odometer, bins=[year_bins, odometer_bins], cmin=1, cmap="Blues")
fig.colorbar(cells, label="Number of listings")
ax.set_title(f"Used car listings up to ${budget:,}, 2021 (n = {len(shown):,})")
ax.set_xlabel("Model year")
ax.set_ylabel("Odometer (miles)")
ax.yaxis.set_major_formatter("{x:,.0f}")
fig.tight_layout()
st.pyplot(fig)
st.caption("Darker cells hold more listings. Craigslist listings from April-May 2021, reposts removed.")
