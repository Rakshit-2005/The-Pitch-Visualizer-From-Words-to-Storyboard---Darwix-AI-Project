"""
Image Generation Module
Generates images from prompts using Hugging Face Stable Diffusion
"""

import torch
from PIL import Image
import os
from typing import List, Optional
import gc

# Delay diffusers import to handle compatibility issues
try:
    from diffusers import StableDiffusionPipeline
    DIFFUSERS_AVAILABLE = True
except ImportError as e:
    DIFFUSERS_AVAILABLE = False
    import warnings
    warnings.warn(f"Diffusers library not available: {e}. Image generation will not work.")


class ImageGenerator:
    """Handles image generation using Stable Diffusion"""
    
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5", use_cpu: bool = False):
        """
        Initialize Stable Diffusion pipeline
        
        Args:
            model_id (str): Hugging Face model ID
            use_cpu (bool): Force CPU usage (slower but doesn't require GPU)
        """
        self.model_id = model_id
        self.use_cpu = use_cpu
        self.device = "cpu" if use_cpu else ("cuda" if torch.cuda.is_available() else "cpu")
        
        print(f"Initializing Stable Diffusion on device: {self.device}")
        print(f"Note: If using CPU, image generation will be slow (2-5 minutes per image)")
        print(f"      GPU will generate images in 10-30 seconds per image")
        
        try:
            # Use fp16 for memory efficiency (if GPU available)
            if self.device == "cuda":
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16,
                    safety_checker=None  # Disable for faster generation
                )
            else:
                # CPU uses float32
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    safety_checker=None
                )
            
            self.pipeline.to(self.device)
            
            # Enable memory optimization
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
        
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            print("Make sure you have enough disk space (~4GB) and stable internet connection")
            raise
    
    def generate_image(self, prompt: str, height: int = 512, width: int = 512, 
                       steps: int = 20) -> Optional[Image.Image]:
        """
        Generate a single image from a prompt
        
        Args:
            prompt (str): Text prompt describing the image
            height (int): Image height (512 or 768)
            width (int): Image width (512 or 768)
            steps (int): Number of inference steps (higher = better quality, slower)
        
        Returns:
            Optional[Image.Image]: Generated PIL Image or None if error
        """
        try:
            print(f"Generating image with prompt: {prompt[:80]}...")
            
            with torch.no_grad():
                image = self.pipeline(
                    prompt,
                    height=height,
                    width=width,
                    num_inference_steps=steps,
                    guidance_scale=7.5
                ).images[0]
            
            print("Image generated successfully!")
            return image
        
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None
    
    def generate_images_batch(self, prompts: List[str], output_dir: str = "outputs",
                             height: int = 512, width: int = 512, 
                             steps: int = 20) -> List[tuple]:
        """
        Generate multiple images from a list of prompts
        
        Args:
            prompts (List[str]): List of text prompts
            output_dir (str): Directory to save images
            height (int): Image height
            width (int): Image width
            steps (int): Number of inference steps
        
        Returns:
            List[tuple]: List of (image_path, PIL_Image) tuples
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n[{i}/{len(prompts)}] Generating image...")
            
            image = self.generate_image(prompt, height, width, steps)
            
            if image:
                # Save image
                image_path = os.path.join(output_dir, f"storyboard_scene_{i:02d}.png")
                image.save(image_path)
                print(f"Saved: {image_path}")
                
                results.append((image_path, image))
            else:
                results.append((None, None))
            
            # Clear GPU memory after each generation
            torch.cuda.empty_cache()
            gc.collect()
        
        return results
    
    def cleanup(self):
        """Free up GPU memory"""
        if hasattr(self, 'pipeline'):
            del self.pipeline
        torch.cuda.empty_cache()
        gc.collect()


def get_generation_params(quality: str = "balanced") -> dict:
    """
    Return recommended parameters based on quality setting
    
    Args:
        quality (str): "fast", "balanced", or "high"
    
    Returns:
        dict: Generation parameters
    """
    params = {
        "fast": {"steps": 15, "height": 512, "width": 512},
        "balanced": {"steps": 20, "height": 512, "width": 512},
        "high": {"steps": 30, "height": 768, "width": 768},
    }
    return params.get(quality, params["balanced"])


if __name__ == "__main__":
    # Example usage (downloads ~4GB model on first run)
    prompts = [
        "A frustrated woman at a desk with outdated computers, looking stressed. Dark. Photorealistic.",
        "A team implementing new software, laptops glowing, focused and collaborative. Bright office. Cinematic.",
        "A happy professional smiling at success, charts showing growth. Warm lighting. Satisfied expression.",
    ]
    
    # Uncomment to test
    # generator = ImageGenerator(use_cpu=False)  # Set to True for CPU
    # results = generator.generate_images_batch(prompts, output_dir="outputs", steps=20)
    # generator.cleanup()
