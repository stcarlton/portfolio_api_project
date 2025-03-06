# services/replicate.py

import os
import replicate

def process_icon_from_prompt(prompt: str) -> str:
    """
    Generates an icon using only a custom prompt (without including the original image).
    """
    try:
        input_data = {
            "prompt": prompt,
            "width": 768,
            "height": 768,
            "refine": "expert_ensemble_refiner",
            "apply_watermark": False,
            "num_inference_steps": 25
        }
        model_version = "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"
        output = replicate.run(model_version, input=input_data)
        # Assuming output returns objects with a .url property
        return list(output)[-1].url

    except Exception as e:
        raise Exception(f"AI Processing Failed: {str(e)}")
