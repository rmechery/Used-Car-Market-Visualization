# CS571 Final Project

Used car market visualization for first-time buyers and sellers.
Team: Ryan Mechery, Skye Iley, Nam Nguyen.

## Run the dashboard

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    streamlit run streamlit_app.py

| Page | Task |
|---|---|
| Find a car within budget | 1.1 |
| Compare models | 1.3 |
| Compare the competition | 2.2 |
| Understand depreciation | 2.3 |

## Layout

    streamlit_app.py        entry point and page navigation
    app/data.py             cached data loaders shared by every page
    app/views/              one file per dashboard page
    data/                   preprocessed parquet files the app reads (committed)
    scripts/prepare_data.py builds data/ from the raw Kaggle CSVs
    docs/                   deliverable write-ups, rubric, and saved figures

## Data

The app only needs the small files in `data/`, which are committed. To rebuild them,
download the raw datasets from Kaggle into the repo root (they are not tracked in git):

- [Used Cars Dataset](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data), saved as `craigslist.csv`
- [Car Features and MSRP](https://www.kaggle.com/datasets/CooperUnion/cardataset), saved as `car_features_and_msrp.csv`

then run `python scripts/prepare_data.py`.

## Deploy (Streamlit Community Cloud)

Push to GitHub, then at [share.streamlit.io](https://share.streamlit.io) create an app from this
repo with branch `main` and main file `streamlit_app.py`. Choose Python 3.11 or newer.
