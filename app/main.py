from fastapi import FastAPI
from app.routes import image, huggingface, openai

app = FastAPI(title="Portfolio API Project")

app.include_router(image.router, prefix="/image", tags=["Image Processing"])
app.include_router(huggingface.router, prefix="/hf")
app.include_router(openai.router, prefix="/openai")

@app.get("/")
def root():
    return {"message": "Welcome to the AI Processing API!"}

