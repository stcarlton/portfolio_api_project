from pydantic import BaseModel

class ImageRequest(BaseModel):
    image_base64: str

class ImageResponse(BaseModel):
    output_url: str

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    generated_text: str