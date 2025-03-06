from pydantic import BaseModel

class ImageRequest(BaseModel):
    image_base64: str

class ImageResponse(BaseModel):
    output_url: str
