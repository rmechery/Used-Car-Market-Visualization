"""Dashboard entry point. Locally: streamlit run streamlit_app.py"""
import streamlit as st

st.set_page_config(page_title="Used Car Market Explorer", page_icon="🚗", layout="wide")

pages = {
    "": [st.Page("app/views/home.py", title="Overview", default=True)],
    "First-time buyer": [
        st.Page("app/views/budget.py", title="Find a car within budget"),
        st.Page("app/views/compare_models.py", title="Compare models"),
    ],
    "Seller": [
        st.Page("app/views/compare_competition.py", title="Compare the competition"),
        st.Page("app/views/depreciation.py", title="Understand depreciation"),
    ],
}
st.navigation(pages).run()
