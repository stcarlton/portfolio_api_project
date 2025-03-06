import base64
import io
import os
import tempfile
import requests
import openai
from PIL import Image

def generate_image_from_prompt(prompt: str, size: str = "1024x1024") -> dict:
    """
    Generates an image using OpenAI's text-to-image endpoint based on the provided prompt.
    """
    print("generating image")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size
    )
    return response

def create_full_mask_from_image(base64_image: str) -> str:
    """
    Generates a fully transparent mask (same dimensions as the input image) in RGBA mode,
    and saves it as a temporary file.
    """
    try:
        image_data = base64.b64decode(base64_image)
        with Image.open(io.BytesIO(image_data)) as image:
            # Convert to RGBA
            image = image.convert("RGBA")
            # Create a fully transparent mask (alpha = 0) with the same dimensions.
            transparent_mask = Image.new("RGBA", image.size, (0, 0, 0, 0))
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png", mode="wb") as temp_mask_file:
                transparent_mask.save(temp_mask_file, format="PNG")
                mask_path = temp_mask_file.name
        return mask_path
    except Exception as e:
        raise Exception(f"Error creating mask: {str(e)}")

def save_image_to_tempfile(base64_image: str) -> str:
    try:
        image_data = base64.b64decode(base64_image)
        with Image.open(io.BytesIO(image_data)) as im:
            im = im.convert("RGBA")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png", mode="wb") as temp_image_file:
                im.save(temp_image_file, format="PNG")
                image_path = temp_image_file.name
        return image_path
    except Exception as e:
        raise Exception(f"Error saving example image: {str(e)}")
   
def edit_image_dalle_from_base64(image_base64: str, prompt: str, size: str = "1024x1024") -> dict:
    """
    Uses DALL-E's image edit endpoint with an example image (converted to RGBA)
    and a fully transparent mask to force a full edit.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Save the base64 image to a temporary file, converting it to RGBA
    try:
        image_path = save_image_to_tempfile(image_base64)
    except Exception as e:
        raise Exception(f"Error saving example image: {str(e)}")
    
    # Generate a fully transparent mask from the image
    try:
        mask_path = create_full_mask_from_image(image_base64)
    except Exception as e:
        os.remove(image_path)
        raise Exception(f"Error generating mask: {str(e)}")
    
    data = {
        "prompt": prompt,
        "n": 1,
        "size": size
    }
    
    with open(image_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
        files = {
            "image": image_file,
            "mask": mask_file
        }
        response = requests.post("https://api.openai.com/v1/images/edits", headers=headers, files=files, data=data)
    
    # Clean up temporary files
    os.remove(image_path)
    os.remove(mask_path)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"DALL-E API Error: {response.text}")