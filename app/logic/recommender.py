import pandas as pd
from math import radians, cos, sin, sqrt, atan2
import os


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in kilometers between two geographic coordinates using the Haversine formula.
    """
    R = 6371  # Radius of Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def load_data():
    """
    Loads supplier, charity, and rating data from the /app/data/ directory.
    """
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    suppliers = pd.read_csv(os.path.join(base_path, 'suppliers.csv'))
    charities = pd.read_csv(os.path.join(base_path, 'charities.csv'))
    ratings = pd.read_csv(os.path.join(base_path, 'ratings.csv'))
    return suppliers, charities, ratings


def get_recommended_suppliers(charity_id: int, max_distance_km: float = 50.0, top_n: int = 5):
    """
    Returns a list of top recommended suppliers based on:
    - average rating from other charities
    - proximity to the given charity's location

    Parameters:
        charity_id: int - ID of the requesting charity
        max_distance_km: float - maximum supplier distance to consider
        top_n: int - number of suppliers to return

    Returns:
        A list of supplier dictionaries sorted by rating and distance
    """
    suppliers, charities, ratings = load_data()

    # Get the location of the requesting charity
    charity = charities[charities['charity_id'] == charity_id]
    if charity.empty:
        return {"error": "Charity not found."}

    charity_lat = charity.iloc[0]['lat']
    charity_lng = charity.iloc[0]['lng']

    # Calculate average rating per supplier
    avg_ratings = ratings.groupby('supplier_id')['rating'].mean().reset_index()
    avg_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)

    # Merge supplier data with average ratings
    merged = pd.merge(suppliers, avg_ratings, on='supplier_id', how='left')
    merged['avg_rating'].fillna(0, inplace=True)

    # Calculate distance between supplier and charity
    merged['distance_km'] = merged.apply(
        lambda row: haversine_distance(charity_lat, charity_lng, row['lat'], row['lng']),
        axis=1
    )

    # Filter suppliers within distance range
    nearby = merged[merged['distance_km'] <= max_distance_km]

    # Sort by highest rating then closest distance
    recommended = nearby.sort_values(by=['avg_rating', 'distance_km'], ascending=[False, True])

    # Return top N results
    result = recommended.head(top_n)[['supplier_id', 'name', 'avg_rating', 'distance_km']]
    return result.to_dict(orient='records')
