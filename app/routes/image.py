from fastapi import APIRouter, HTTPException
from app.models.models import ImageRequest, ImageResponse
from app.services.caption import label_sketch
from app.services.replicate import process_icon_from_prompt
from fastapi import APIRouter, HTTPException
from app.models.models import ImageRequest, ImageResponse
from app.services.openai import edit_image_dalle_from_base64
from app.services.gpt4o_mini import generate_description_from_image
from app.services.openai import generate_image_from_prompt

router = APIRouter()

@router.post("/generate-icon", response_model=ImageResponse)
async def generate_icon_two_tier(request: ImageRequest):
    """
    Two-tier endpoint:
    1. Uses GPT‑4o mini to generate a detailed description of the input sketch.
    2. Uses that description in a refined prompt to generate a new icon via DALL‑E's text-to-image endpoint.
    """
    print("received request to generate icon")
    try:
        # Tier 1: Get a detailed description from GPT‑4o mini.
        description = generate_description_from_image(request.image_base64)
        
        # Tier 2: Build a refined prompt that includes the description.
        refined_prompt = (
            f"Using the following description of a sketch: '{description}', generate a clean, minimalist, "
            f"vector-style icon. The icon should have a transparent background, crisp lines, and be suitable "
            f"for modern web development."
        )
        
        # Generate the image using the text-to-image endpoint.
        dalle_response = generate_image_from_prompt(refined_prompt, size="1024x1024")
        image_url = dalle_response["data"][0]["url"]
        print("returning")
        return {"output_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-icon-dalle", response_model=ImageResponse)
async def generate_icon_dalle(request: ImageRequest):
    """
    Endpoint using DALL-E's image edit endpoint with an example image and a full mask.
    """
    print("received request to generate icon")
    try:
        prompt = (
            "The image is a sketch drawn by hand. This image should be transformed into a clean, modern, minimalist icon that preserves the original shape and structure that still resembles the image. Enhance the line precision, remove extraneous details, and improve clarity."
        )
        # Call the DALL-E edit endpoint function
        dalle_response = edit_image_dalle_from_base64(request.image_base64, prompt, size="1024x1024")
        # Process the response – assuming the response contains a "data" field with a URL
        image_url = dalle_response["data"][0]["url"]
        print("returning")
        return {"output_url": image_url}
    
    except Exception as e:
        print(f"error in generate_icon_dalle:{e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-icon-replicate", response_model=ImageResponse)
async def generate_icon_abstracted(request: ImageRequest):
    """
    New endpoint that first abstracts the sketch then generates a clean icon without including the original image.
    """
    try:
        # Step 1: Label the sketch
        abstraction = label_sketch(request.image_base64)
        if not abstraction:
            raise Exception("Unable to determine the subject of the sketch.")
        
        # Optionally, simplify the caption to a core label.
        # This is a placeholder strategy—you might apply more robust NLP processing here.
        simple_abstraction = abstraction.split()[-1]
        
        # Step 2: Create a refined prompt using the abstraction
        refined_prompt = (
            f"Generate a clean, minimalist, vector-style icon of a {simple_abstraction}. "
            "The icon should have a transparent background, crisp lines, and be suitable for modern web development."
        )
        
        # Step 3: Generate the icon using only the refined prompt
        image_url = process_icon_from_prompt(refined_prompt)
        return {"output_url": image_url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
