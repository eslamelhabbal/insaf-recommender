from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Supplier Recommendation API",
    version="1.0",
    description="Suggests top suppliers for a given charity based on ratings and distance."
)

# Include the API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)