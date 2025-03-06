import openai
import base64
import tempfile
import os
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def generate_description_from_image(base64_image: str) -> str:
    """
    Uses GPT‑4o mini to generate a detailed description of the input sketch.
    Expects a base64-encoded image.
    """
    print("classifying image")
    try:
        # Set your OpenAI API key from the environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise Exception("Missing OpenAI API key. Please set it in your .env file.")

        # Decode the base64 image and save it to a temporary file.
        image_data = base64.b64decode(base64_image)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(image_data)
            tmp_file_path = tmp_file.name

        # Open the temporary file in binary mode.
        with open(tmp_file_path, "rb") as image_file:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Please analyze the attached chicken scratch sketch. "
                            "Identify what the artist is trying to convey and any important details required to reproduce a clean, minimalist icon."
                        ),
                        "image": image_file  # This assumes the API supports an "image" field.
                    }
                ]
            )

        # Clean up the temporary image file.
        os.remove(tmp_file_path)

        # Extract and return the description.
        description = response["choices"][0]["message"]["content"]
        print(description)
        return description
    except Exception as e:
        print(e)
        raise Exception(f"Error classifying image: {str(e)}")
