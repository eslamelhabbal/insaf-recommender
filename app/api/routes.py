from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import csv
import os
from app.logic.recommender import recommend_suppliers_for_charity


router = APIRouter()

# Paths to CSV files
CHARITIES_FILE = "app/data/charities.csv"
SUPPLIERS_FILE = "app/data/suppliers.csv"
RATINGS_FILE = "app/data/ratings.csv"

# Pydantic models
class Recommendation(BaseModel):
    supplier_id: int
    name: str
    score: float
    distance_km: float

class NewCharity(BaseModel):
    charity_id: int
    name: str
    lat: float
    lng: float

class NewSupplier(BaseModel):
    supplier_id: int
    name: str
    lat: float
    lng: float

class NewRating(BaseModel):
    charity_id: int
    supplier_id: int
    rating: int  # from 1 to 5

# Routes

@router.get("/recommendations/{charity_id}")
def get_recommendations(charity_id: int):
    return recommend_suppliers_for_charity(charity_id)


@router.post("/charities", status_code=201)
def add_charity(charity: NewCharity):
    if not os.path.exists(CHARITIES_FILE):
        raise HTTPException(status_code=500, detail="Charities file not found.")
    with open(CHARITIES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["charity_id"]) == charity.charity_id:
                raise HTTPException(status_code=400, detail="Charity ID already exists.")
    with open(CHARITIES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([charity.charity_id, charity.name, charity.lat, charity.lng])
    return {"message": "Charity added successfully ✅"}

@router.post("/suppliers", status_code=201)
def add_supplier(supplier: NewSupplier):
    if not os.path.exists(SUPPLIERS_FILE):
        raise HTTPException(status_code=500, detail="Suppliers file not found.")
    with open(SUPPLIERS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["supplier_id"]) == supplier.supplier_id:
                raise HTTPException(status_code=400, detail="Supplier ID already exists.")
    with open(SUPPLIERS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([supplier.supplier_id, supplier.name, supplier.lat, supplier.lng])
    return {"message": "Supplier added successfully ✅"}

@router.post("/ratings", status_code=201)
def add_rating(rating_obj: NewRating):
    if rating_obj.rating < 1 or rating_obj.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
    if not os.path.exists(RATINGS_FILE):
        raise HTTPException(status_code=500, detail="Ratings file not found.")
    with open(RATINGS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                int(row["charity_id"]) == rating_obj.charity_id and
                int(row["supplier_id"]) == rating_obj.supplier_id
            ):
                raise HTTPException(status_code=400, detail="Rating already exists for this pair.")
    with open(RATINGS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([rating_obj.charity_id, rating_obj.supplier_id, rating_obj.rating])
    return {"message": "Rating added successfully ✅"}

@router.get("/charities")
def list_charities():
    if not os.path.exists(CHARITIES_FILE):
        raise HTTPException(status_code=500, detail="Charities file not found.")

    charities = []
    with open(CHARITIES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            charities.append({
                "charity_id": int(row["charity_id"]),
                "name": row["name"],
                "lat": float(row["lat"]),
                "lng": float(row["lng"])
            })
    return charities

@router.get("/suppliers")
def list_suppliers():
    if not os.path.exists(SUPPLIERS_FILE):
        raise HTTPException(status_code=500, detail="Suppliers file not found.")

    suppliers = []
    with open(SUPPLIERS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            suppliers.append({
                "supplier_id": int(row["supplier_id"]),
                "name": row["name"],
                "lat": float(row["lat"]),
                "lng": float(row["lng"])
            })
    return suppliers

@router.get("/ratings")
def list_ratings(charity_id: int = None, supplier_id: int = None):
    if not os.path.exists(RATINGS_FILE):
        raise HTTPException(status_code=500, detail="Ratings file not found.")

    ratings = []
    with open(RATINGS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                "charity_id": int(row["charity_id"]),
                "supplier_id": int(row["supplier_id"]),
                "rating": int(row["rating"])
            }
            if charity_id is not None and record["charity_id"] != charity_id:
                continue
            if supplier_id is not None and record["supplier_id"] != supplier_id:
                continue
            ratings.append(record)
    return ratings
@router.get("/")
def root():
    return {"message": "Welcome to Insaf Recommender API"}
