# services/caption.py

import base64
import io
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize and cache the processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def label_sketch(base64_image: str) -> str:
    """
    Converts a Base64-encoded sketch to a caption.
    You might post-process the caption to extract a simple label.
    """
    try:
        # Decode the image and convert to a PIL image
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        # Generate a caption
        inputs = processor(image, return_tensors="pt")
        output_ids = model.generate(**inputs)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        
        print(caption)
        return caption
    except Exception as e:
        print(f"Error labeling sketch: {str(e)}")
        return ""
