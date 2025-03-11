from fastapi import APIRouter
from pydantic import BaseModel
from app.models.models import GenerateResponse, GenerateRequest
from app.services.huggingface import HuggingFaceService

router = APIRouter()

hf_service = HuggingFaceService()

@router.post("/generate-text-hf", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    print("Reqeust to generate text received.")
    generated_text = await hf_service.generate_text(request.prompt)
    return GenerateResponse(generated_text=generated_text)
