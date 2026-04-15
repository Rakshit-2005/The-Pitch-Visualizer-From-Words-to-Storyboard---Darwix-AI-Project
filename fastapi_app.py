"""
Pitch Visualizer - FastAPI Application
Alternative server implementation using FastAPI + Jinja2 templates.
"""

import os
import traceback
from datetime import datetime
from typing import Literal

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from pydantic import BaseModel

from text_processor import segment_text, validate_text_input
from image_generator import ImageGenerator, get_generation_params, DIFFUSERS_AVAILABLE
from storyboard_generator import StoryboardGenerator


BASE_DIR = os.path.dirname(__file__)
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=DOTENV_PATH, override=True)

OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
NEGATIVE_PROMPT = (
    "low quality, blurry, distorted face, deformed body, extra limbs, text, letters, words, captions, "
    "watermark, logo, UI, screenshot, collage, split screen, tiled layout, cropped, jpeg artifacts, noisy"
)


def get_gemini_api_key() -> str:
    key = (os.getenv("GEMINI_API_KEY") or "").strip()
    return key.strip('"').strip("'")


def create_simple_prompt(sentence: str, style: str = "photorealistic") -> str:
    style_keywords = {
        "photorealistic": "photorealistic, high detail, cinematic lighting, professional",
        "cartoon": "animated, bright colors, cartoon style, playful",
        "watercolor": "watercolor painting, soft edges, artistic",
        "digital art": "digital art, vibrant, modern, high quality",
        "oil painting": "oil painting, classical, detailed",
        "sketch": "pencil sketch, artistic, minimalist",
    }
    keywords = style_keywords.get(style, style_keywords["photorealistic"])
    return f"{sentence} Visual style: {keywords}, attention to emotion and atmosphere."


def to_render_prompt(prompt_text: str, style: str) -> str:
    """Normalize prompts for cleaner, single-frame image generation."""
    style_map = {
        "photorealistic": "photorealistic cinematic photography",
        "cartoon": "high-quality cartoon illustration",
        "watercolor": "watercolor painting",
        "digital art": "digital concept art",
        "oil painting": "classical oil painting",
        "sketch": "detailed pencil sketch",
    }
    style_phrase = style_map.get(style, "photorealistic cinematic photography")
    return (
        "Single scene, one moment, one setting. "
        f"{prompt_text}. "
        f"Style: {style_phrase}. "
        "Professional composition, clean subject focus, realistic proportions, no text in image."
    )


class GenerateRequest(BaseModel):
    text: str
    style: str = "photorealistic"
    use_api: bool = True
    quality: Literal["fast", "balanced", "high"] = "balanced"


app = FastAPI(title="Pitch Visualizer", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/status")
def status():
    gemini_api_key = get_gemini_api_key()
    return {
        "status": "online",
        "gemini_configured": bool(gemini_api_key),
        "image_generation_available": bool(DIFFUSERS_AVAILABLE),
    }


@app.get("/api/styles")
def get_styles():
    return {
        "styles": [
            "photorealistic",
            "cartoon",
            "watercolor",
            "digital art",
            "oil painting",
            "sketch",
        ]
    }


@app.post("/api/generate")
def generate_storyboard(payload: GenerateRequest):
    try:
        text = payload.text.strip()
        style = payload.style
        use_api = payload.use_api

        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        segments = segment_text(text)

        if use_api:
            gemini_api_key = get_gemini_api_key()
            if not gemini_api_key:
                raise HTTPException(
                    status_code=400,
                    detail="Gemini API key not configured. Add GEMINI_API_KEY in .env or disable Use API.",
                )

            prompts = []
            for seg in segments:
                prompt_instruction = (
                    "You are an expert visual prompt engineer. Convert the narrative into one clean cinematic "
                    "single-frame image prompt. Mention subject, setting, camera framing, lighting, mood, "
                    "and key visual details. Avoid UI/screenshot aesthetics and avoid text in image. "
                    "Return exactly one prompt sentence. "
                    f"Style: {style}. Scene: {seg}"
                )
                response = requests.post(
                    GEMINI_API_URL,
                    params={"key": gemini_api_key},
                    headers={"Content-Type": "application/json"},
                    json={"contents": [{"parts": [{"text": prompt_instruction}]}]},
                    timeout=30,
                )
                if response.status_code != 200:
                    fallback_prompt = create_simple_prompt(seg, style)
                    prompts.append(fallback_prompt)
                    continue

                result = response.json()
                try:
                    generated = result["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError, TypeError):
                    generated = create_simple_prompt(seg, style)
                prompts.append(to_render_prompt(generated, style))
        else:
            prompts = [to_render_prompt(create_simple_prompt(seg, style), style) for seg in segments]

        if not DIFFUSERS_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Image generation backend is not available. Fix diffusers/transformers versions or run Flask fallback app.",
            )

        generator = ImageGenerator(use_cpu=False)
        image_results = []
        try:
            gen_params = get_generation_params(payload.quality)
            image_results = generator.generate_images_batch(
                prompts,
                output_dir=OUTPUTS_DIR,
                negative_prompt=NEGATIVE_PROMPT,
                **gen_params,
            )
        finally:
            generator.cleanup()

        image_paths = [path for path, _ in image_results if path is not None]
        if not image_paths:
            raise HTTPException(status_code=500, detail="Failed to generate images for all scenes.")

        storyboard_gen = StoryboardGenerator(OUTPUTS_DIR)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"storyboard_{timestamp}.html"

        storyboard_gen.create_storyboard(
            image_paths,
            segments[:len(image_paths)],
            title="Pitch Visualizer Storyboard",
            style=style,
            filename=filename,
        )

        return {
            "success": True,
            "storyboard_url": f"/outputs/{filename}",
            "scene_count": len(segments),
            "style": style,
            "prompts": prompts,
        }
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        print(str(exc))
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(exc)})


@app.get("/outputs/{filename}")
def serve_output(filename: str):
    file_path = os.path.join(OUTPUTS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="text/html")


if __name__ == "__main__":
    import uvicorn

    gemini_api_key = get_gemini_api_key()
    print("Starting FastAPI server...")
    print("Open: http://localhost:5001")
    print(f"Gemini API Configured: {bool(gemini_api_key)}")

    uvicorn.run(app, host="0.0.0.0", port=5001)
