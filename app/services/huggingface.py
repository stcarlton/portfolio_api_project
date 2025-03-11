import os
import httpx
from fastapi import HTTPException

class HuggingFaceService:
    def __init__(self, model_name: str = "EleutherAI/gpt-j-6B"):
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.api_token = os.getenv("HF_API_TOKEN")
        if not self.api_token:
            raise ValueError("HF_API_TOKEN environment variable is not set")

    async def generate_text(self, prompt: str, max_new_tokens: int = 50) -> str:
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": 0.9,
                "do_sample": True,
                "top_p": 0.9,
                "repetition_penalty": 1.2
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        data = response.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return "No output returned"
