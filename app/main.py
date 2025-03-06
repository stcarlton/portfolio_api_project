from fastapi import FastAPI
from app.routes import image

app = FastAPI(title="Portfolio API Project")

# Register image processing routes
app.include_router(image.router, prefix="/image", tags=["Image Processing"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI Processing API!"}

