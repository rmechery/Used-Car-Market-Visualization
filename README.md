# CS571 Final Project

Used car market visualization for first-time buyers and sellers.
Team: Ryan Mechery, Skye Iley, Nam Nguyen.

## Setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Data

Not tracked in git. Download these from Kaggle and place them in the repo root:

- [Used Cars Dataset](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data), saved as `craigslist.csv`
- [Car Features and MSRP](https://www.kaggle.com/datasets/CooperUnion/cardataset), saved as `car_features_and_msrp.csv`

## Deliverable 1 figures

    python deliverable_1/make_figures.py    # task 1.1: saves a PNG to deliverable_1/output/
    streamlit run deliverable_1/app.py      # task 1.3: model comparison page
