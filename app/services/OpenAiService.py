import os
import asyncio
from fastapi import HTTPException
from openai import OpenAI

class OpenAiService:
    def __init__(self, model: str = "gpt-4o"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        # Instantiate the new OpenAI client.
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    async def generate_text(self, prompt: str, max_tokens: int = 150, temperature: float = 0.7) -> str:
        # Prepare the messages according to the new interface.
        messages = [
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        loop = asyncio.get_event_loop()
        try:
            # Wrap the synchronous API call in an executor.
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            )
            # Extract the generated text from the response.
            generated_text = response.choices[0].message
            return generated_text.strip() if isinstance(generated_text, str) else str(generated_text).strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")
