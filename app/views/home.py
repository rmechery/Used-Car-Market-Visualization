import streamlit as st

from app.data import load_listings

st.title("Used Car Market Explorer")
st.write(
    "Explore 2021 Craigslist used car listings, joined with manufacturer specs and MSRP, "
    "to help first-time buyers and sellers make sense of the market."
)
st.metric("Listings after cleaning", f"{len(load_listings()):,}")

buyer, seller = st.columns(2)
with buyer:
    st.subheader("First-time buyer")
    st.page_link("app/views/budget.py", label="1.1 Find a car within budget")
    st.page_link("app/views/compare_models.py", label="1.3 Compare models")
with seller:
    st.subheader("Seller")
    st.page_link("app/views/compare_competition.py", label="2.2 Compare the competition")
    st.page_link("app/views/depreciation.py", label="2.3 Understand depreciation")

st.caption(
    "Data: [Used Cars Dataset](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data) and "
    "[Car Features and MSRP](https://www.kaggle.com/datasets/CooperUnion/cardataset) on Kaggle. "
    "CS571 final project by Ryan Mechery, Skye Iley, and Nam Nguyen."
)
