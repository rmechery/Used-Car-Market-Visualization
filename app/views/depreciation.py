"""Task 2.3: how does a model's retained value (price / MSRP) drop with age and mileage?"""
import altair as alt
import pandas as pd
import streamlit as st

from app.data import BLUE, SNAPSHOT_YEAR, load_matched_listings, load_specs

MIN_PER_POINT = 10  # hide age or mileage groups with fewer listings than this
MILEAGE_BIN = 40_000


@st.cache_data
def load_retained_value():
    """Listings joined to MSRP by make, model, and model year (MSRP data covers 1990-2017)."""
    msrp = load_specs()[["manufacturer", "model", "year", "msrp"]]
    df = load_matched_listings().merge(msrp, on=["manufacturer", "model", "year"])
    df["retained"] = df.price / df.msrp
    df["age"] = SNAPSHOT_YEAR - df.year
    # Drop implausible ratios (typos, parts cars, MSRP mismatches).
    return df[df.retained.between(0.05, 1.5)]


def trend(df, column):
    stats = df.groupby(column).retained.agg(
        median="median", q1=lambda s: s.quantile(0.25), q3=lambda s: s.quantile(0.75), n="size"
    )
    return stats[stats.n >= MIN_PER_POINT].reset_index()


def chart(stats, column, title, axis_format):
    base = alt.Chart(stats).encode(
        x=alt.X(f"{column}:Q", title=title, axis=alt.Axis(format=axis_format, tickMinStep=1)),
    )
    y_axis = alt.Axis(format=".0%", title="Retained value (price / MSRP)")
    band = base.mark_area(opacity=0.25, color=BLUE).encode(y=alt.Y("q1:Q", axis=y_axis), y2="q3:Q")
    tooltip = [
        alt.Tooltip(f"{column}:Q", title=title, format=axis_format),
        alt.Tooltip("median:Q", title="Median retained", format=".0%"),
        alt.Tooltip("q1:Q", title="25th percentile", format=".0%"),
        alt.Tooltip("q3:Q", title="75th percentile", format=".0%"),
        alt.Tooltip("n:Q", title="Listings"),
    ]
    line = base.mark_line(color=BLUE, strokeWidth=2).encode(y="median:Q")
    points = base.mark_circle(color=BLUE, size=70, opacity=1).encode(y="median:Q", tooltip=tooltip)
    labels = base.mark_text(dy=-12, color="#333", fontSize=11).encode(y="median:Q", text=alt.Text("median:Q", format=".0%"))
    return (band + line + points + labels).properties(height=360)


st.title("Understand depreciation")
st.caption("Task 2.3 · seller")

df = load_retained_value()
counts = df.car.value_counts()
cars = sorted(counts[counts >= 50].index)
left, right = st.columns([2, 3])
car = left.selectbox("Make and model", cars, index=cars.index("Toyota Corolla") if "Toyota Corolla" in cars else 0)
model = df[df.car == car]
years = sorted(model.year.unique())
default = (years[max(0, len(years) - 3)], years[-1])
first, last = right.select_slider("Model years", years, value=default) if len(years) > 1 else (years[0], years[0])

shown = model[model.year.between(first, last)].copy()
shown["mileage"] = (shown.odometer // MILEAGE_BIN) * MILEAGE_BIN + MILEAGE_BIN / 2
by_age, by_mileage = trend(shown, "age"), trend(shown, "mileage")
if by_age.empty and by_mileage.empty:
    st.info("Not enough listings for this selection. Try widening the model years.")
    st.stop()

st.markdown(f"**{car}: retained value by age and mileage**  \n"
            f"Craigslist listings, 2021, model years {first}-{last} (n = {len(shown):,})")
combined = alt.hconcat(
    chart(by_age, "age", "Age (years)", "d"),
    chart(by_mileage, "mileage", "Odometer (miles)", ",.0f"),
).resolve_scale(y="shared")
st.altair_chart(combined, width="stretch")
st.caption(
    "Line shows the median listing price as a share of the original MSRP; the band covers the middle 50% "
    f"of listings. Mileage is grouped into {MILEAGE_BIN:,}-mile bins. Groups with fewer than "
    f"{MIN_PER_POINT} listings are hidden. A steeper drop marks where depreciation accelerates."
)
with st.expander("Data table"):
    st.dataframe(pd.concat({"By age": by_age.set_index("age"), "By mileage": by_mileage.set_index("mileage")}))
