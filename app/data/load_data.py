import pandas as pd
import os

# Define paths relative to the app/data directory
DATA_DIR = os.path.dirname(__file__)
CHARITIES_FILE = os.path.join(DATA_DIR, "charities.csv")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.csv")
RATINGS_FILE = os.path.join(DATA_DIR, "ratings.csv")


def load_charities():
    return pd.read_csv(CHARITIES_FILE)


def load_suppliers():
    return pd.read_csv(SUPPLIERS_FILE)


def load_ratings():
    return pd.read_csv(RATINGS_FILE)