
import pandas as pd
import math
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

CHARITIES_FILE = os.path.join(DATA_DIR, "charities.csv")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.csv")
RATINGS_FILE = os.path.join(DATA_DIR, "ratings.csv")


def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two geo coordinates
    R = 6371  # Radius of Earth in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def load_data():
    charities = pd.read_csv(CHARITIES_FILE)
    suppliers = pd.read_csv(SUPPLIERS_FILE)
    ratings = pd.read_csv(RATINGS_FILE)
    return charities, suppliers, ratings


def recommend_suppliers_for_charity(charity_id: int, top_n: int = 5):
    charities, suppliers, ratings = load_data()

    # Check if charity exists
    if charity_id not in charities["charity_id"].values:
        return []

    # Get charity location safely
    charity_row = charities[charities["charity_id"] == charity_id]
    if charity_row.empty:
        return []

    charity_row = charity_row.iloc[0]
    charity_lat = charity_row["lat"]
    charity_lng = charity_row["lng"]

    # Calculate average ratings
    avg_ratings = ratings.groupby("supplier_id")["rating"].mean().reset_index()
    avg_ratings.columns = ["supplier_id", "avg_rating"]

    # Merge with suppliers
    merged = suppliers.merge(avg_ratings, on="supplier_id", how="left").fillna(0)

    # Compute distance to each supplier
    merged["distance_km"] = merged.apply(
        lambda row: haversine(charity_lat, charity_lng, row["lat"], row["lng"]), axis=1
    )

    # Score = rating / distance
    merged["score"] = merged["avg_rating"] / (merged["distance_km"] + 1e-5)

    # Sort by score descending
    top_suppliers = merged.sort_values("score", ascending=False).head(top_n)

    # Return top suppliers as list of dicts
    return top_suppliers[["supplier_id", "name", "avg_rating", "distance_km"]].to_dict(orient="records")

