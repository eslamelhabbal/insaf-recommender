# Insaf Recommender System

This project provides a recommendation API for charities to find the best nearby suppliers based on:

- Past ratings from other charities
- Geographic distance between the charity and suppliers

## 📦 Tech Stack

- Python 3.10
- FastAPI
- pandas
- Docker (optional)

---

## 🚀 How to Run Locally

```bash
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate    # Windows
source venv/bin/activate   # macOS/Linux

# Install requirements
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
