from fastapi import APIRouter
from pydantic import BaseModel
from app.models.models import GenerateResponse, GenerateRequest
from app.services.OpenAiService import OpenAiService

router = APIRouter()
openai_service = OpenAiService()

@router.post("/generate-text", response_model=GenerateResponse)
async def generate_text_endpoint(request: GenerateRequest):
    print(f"Received request: {request.prompt}")
    generated_text = await openai_service.generate_text(request.prompt)
    return GenerateResponse(generated_text=generated_text)
