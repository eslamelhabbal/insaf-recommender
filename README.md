# Insaf Recommender System

A simple supplier recommendation system for charities, built with FastAPI and powered by CSV files (no database). This system suggests the top suppliers for a charity based on location and ratings.

## 📁 Project Structure

```
.
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── data/
│   │   ├── charities.csv
│   │   ├── suppliers.csv
│   │   ├── ratings.csv
│   │   └── load_data.py
│   └── logic/
│       └── recommender.py
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
└── README.md
```

## 🚀 Run with Docker

Make sure Docker is installed and running.

1. Build and run using Docker Compose:

```bash
docker-compose up --build
```

2. The API will be available at:

- http://localhost:8000  
- http://localhost:8000/docs ← (Swagger UI)

## 📦 Requirements

Used in the Dockerfile:

- fastapi
- uvicorn
- pandas
- scikit-surprise

## 🧪 Example API Usage

Get top 5 supplier recommendations for charity with ID 1:

```
GET /recommendations/1
```

Or with query parameter:

```
GET /recommendations/1?top_n=3
```

## 👨‍💻 Development Notes

- Data is loaded from CSV files on app startup
- The recommendation is based on rating and distance (Haversine formula)
- You can also add new charities, suppliers, and ratings through POST endpoints