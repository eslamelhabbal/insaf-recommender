from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Supplier Recommendation API")

app.include_router(router, prefix="/api")
