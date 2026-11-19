"""Task 2.2: is the seller's car newer, lower-mileage, or in better condition than similar listings?"""
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from app.data import ACCENT, CONDITIONS, GRAY, load_matched_listings

YEAR_WINDOW = 2  # comparables are the same model within +/- this many model years
MIN_COMPARABLES = 20

st.title("Compare your car to the competition")
st.caption("Task 2.2 · seller")

listings = load_matched_listings()
counts = listings.car.value_counts()
cars = sorted(counts[counts >= MIN_COMPARABLES].index)

c1, c2, c3 = st.columns(3)
car = c1.selectbox("Make and model", cars, index=cars.index("Honda Civic") if "Honda Civic" in cars else 0)
model_listings = listings[listings.car == car]
years = sorted(model_listings.year.unique())
year = c2.selectbox("Model year", years, index=years.index(2012) if 2012 in years else len(years) - 1)
condition = c3.selectbox("Condition", CONDITIONS, index=CONDITIONS.index("excellent"))
c4, c5 = st.columns(2)
price = c4.number_input("Your asking price ($)", 500, 250_000, 10_000, step=500)
mileage = c5.number_input("Your mileage (miles)", 0, 500_000, 89_320, step=1_000)

comps = model_listings[model_listings.year.between(year - YEAR_WINDOW, year + YEAR_WINDOW)]
if len(comps) < MIN_COMPARABLES:
    st.info(f"Only {len(comps)} comparable listings for a {year} {car}. Try a more common model or year.")
    st.stop()


def pct(mask):
    return 100 * mask.mean()


def describe(series, value, more, less):
    """'more than X%' when the car sits above most comparables, otherwise 'less than Y%'."""
    below, above = pct(series < value), pct(series > value)
    return f"{more} than {below:.0f}% of comparables" if below >= above else f"{less} than {above:.0f}% of comparables"


def histogram(ax, values, mine, title, fmt):
    q1, med, q3 = np.percentile(values, [25, 50, 75])
    low, high = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    top = max(np.percentile(values, 99.5), mine) * 1.02
    left = min(values.min(), mine)
    ax.hist(values[values <= top], bins=30, range=(left, top), color=GRAY, edgecolor="white", linewidth=0.5)
    if low > left:
        ax.axvspan(left, low, color="#eeeeee", zorder=0, label="Outlier range (1.5 × IQR)")
    if high < top:
        ax.axvspan(high, top, color="#eeeeee", zorder=0, label=None if low > left else "Outlier range (1.5 × IQR)")
    ax.axvline(med, color="black", linestyle="--", linewidth=1, label=f"Median {fmt(med)}")
    ax.axvline(mine, color=ACCENT, linewidth=2, label=f"Your car {fmt(mine)}")
    ax.set_xlim(left, top)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel("Listings")
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_major_formatter(lambda x, _: fmt(x))
    ax.legend(fontsize=7, frameon=False, loc="upper right")


def bars(ax, labels, heights, highlight, title):
    colors = [ACCENT if label == highlight else GRAY for label in labels]
    ax.bar([str(label) for label in labels], heights, color=colors)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel("Listings")


dollars = lambda x: f"${x:,.0f}"
miles = lambda x: f"{x:,.0f} mi"

fig, axes = plt.subplots(2, 2, figsize=(11, 8))
fig.suptitle(
    f"Your {year} {car} vs {len(comps):,} comparable listings ({year - YEAR_WINDOW}-{year + YEAR_WINDOW} model years)\n"
    f"{dollars(price)} · {miles(mileage)} · condition: {condition}",
    fontsize=11,
)
histogram(axes[0, 0], comps.price, price, f"Price: {describe(comps.price, price, 'higher', 'lower')}", dollars)
histogram(axes[0, 1], comps.odometer, mileage, f"Mileage: {describe(comps.odometer, mileage, 'higher', 'lower')}", miles)

year_counts = comps.year.value_counts().reindex(range(year - YEAR_WINDOW, year + YEAR_WINDOW + 1), fill_value=0)
bars(axes[1, 0], year_counts.index, year_counts.values, year,
     f"Model year: newer than {pct(comps.year < year):.0f}% of comparables, older than {pct(comps.year > year):.0f}%")

rated = comps.condition.dropna()
rank = CONDITIONS.index(condition)
codes = rated.cat.codes
condition_counts = rated.value_counts().reindex(CONDITIONS, fill_value=0)
bars(axes[1, 1], CONDITIONS, condition_counts.values, condition,
     f"Condition: better than {pct(codes < rank):.0f}% of rated comparables, worse than {pct(codes > rank):.0f}%\n"
     f"({len(rated):,} of {len(comps):,} state a condition)")

fig.tight_layout()
st.pyplot(fig)
st.caption("Comparables: Craigslist listings from 2021 for the same make and model within "
           f"±{YEAR_WINDOW} model years. Shaded areas fall outside 1.5 × IQR and are likely outliers.")
