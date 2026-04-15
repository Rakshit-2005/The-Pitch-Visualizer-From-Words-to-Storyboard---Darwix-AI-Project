"""
Pitch Visualizer - Flask Web Application
Main application that orchestrates text segmentation, prompt engineering, and image generation
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = os.path.dirname(__file__)
DOTENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=DOTENV_PATH, override=True)

from text_processor import segment_text, validate_text_input
try:
    from prompt_engineer import PromptEngineer, create_simple_prompt, GEMINI_AVAILABLE as PROMPT_ENGINEER_GEMINI_AVAILABLE
except ImportError:
    # Fallback if Gemini API has compatibility issues
    PromptEngineer = None
    PROMPT_ENGINEER_GEMINI_AVAILABLE = False
    from prompt_engineer import create_simple_prompt
from image_generator import ImageGenerator, get_generation_params
from storyboard_generator import StoryboardGenerator

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create outputs directory
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Global variables to handle multiple requests
current_task = None
NEGATIVE_PROMPT = (
    "low quality, blurry, distorted face, deformed body, extra limbs, text, letters, words, captions, "
    "watermark, logo, UI, screenshot, collage, split screen, tiled layout, cropped, jpeg artifacts, noisy"
)


def to_render_prompt(prompt_text: str, style: str) -> str:
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


def get_gemini_api_key():
    key = (os.environ.get('GEMINI_API_KEY') or '').strip()
    return key.strip('"').strip("'")


@app.route('/')
def index():
    """Render home page"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_storyboard():
    """
    API endpoint to generate storyboard
    Expects: {
        "text": "narrative text",
        "style": "photorealistic|cartoon|watercolor|digital art|oil painting|sketch",
        "use_api": true/false (use Gemini API vs fallback),
        "quality": "fast|balanced|high"
    }
    """
    try:
        data = request.json
        text = data.get('text', '').strip()
        style = data.get('style', 'photorealistic')
        use_api = data.get('use_api', True)
        quality = data.get('quality', 'balanced')
        
        # Validate input
        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Segment text
        print(f"[1/5] Segmenting text...")
        segments = segment_text(text)
        print(f"Found {len(segments)} scenes")
        
        # Enhance prompts
        print(f"[2/5] Engineering prompts...")
        if use_api:
            if PromptEngineer is None:
                # Fallback if Gemini API is not available
                prompts = [to_render_prompt(create_simple_prompt(seg, style), style) for seg in segments]
            else:
                api_key = get_gemini_api_key()
                if not api_key:
                    return jsonify({
                        'error': 'Gemini API key not configured. Please set GEMINI_API_KEY environment variable.',
                        'fallback': True
                    }), 400

                if not PROMPT_ENGINEER_GEMINI_AVAILABLE:
                    prompts = [to_render_prompt(create_simple_prompt(seg, style), style) for seg in segments]
                else:
                    try:
                        engineer = PromptEngineer(api_key)
                        prompts = [to_render_prompt(p, style) for p in engineer.enhance_prompts_batch(segments, style)]
                    except Exception:
                        # If SDK fails at runtime (e.g. Python version/protobuf issues), continue with fallback prompts.
                        prompts = [to_render_prompt(create_simple_prompt(seg, style), style) for seg in segments]
        else:
            # Use fallback method
            prompts = [to_render_prompt(create_simple_prompt(seg, style), style) for seg in segments]
        
        # Generate images
        print(f"[3/5] Generating images...")
        generator = ImageGenerator(use_cpu=False)  # Set to True for CPU-only
        gen_params = get_generation_params(quality)
        image_results = generator.generate_images_batch(
            prompts,
            output_dir=OUTPUTS_DIR,
            negative_prompt=NEGATIVE_PROMPT,
            **gen_params
        )
        generator.cleanup()
        
        # Filter successful images
        image_paths = [path for path, _ in image_results if path is not None]
        if not image_paths:
            return jsonify({'error': 'Failed to generate any images'}), 500
        
        # Create storyboard
        print(f"[4/5] Creating storyboard...")
        storyboard_gen = StoryboardGenerator(OUTPUTS_DIR)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"storyboard_{timestamp}.html"
        
        storyboard_path = storyboard_gen.create_storyboard(
            image_paths,
            segments[:len(image_paths)],  # Match captions to images
            title="Pitch Visualizer Storyboard",
            style=style,
            filename=filename
        )
        
        # Get relative path for serving
        relative_path = os.path.relpath(storyboard_path, OUTPUTS_DIR)
        
        return jsonify({
            'success': True,
            'storyboard_url': f'/outputs/{filename}',
            'image_count': len(image_paths),
            'style': style,
            'segments': segments[:len(image_paths)]
        }), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/outputs/<filename>')
def serve_output(filename):
    """Serve generated files"""
    try:
        return send_from_directory(OUTPUTS_DIR, filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404


@app.route('/api/status')
def status():
    """Check API status"""
    gemini_api_key = get_gemini_api_key()
    return jsonify({
        'status': 'online',
        'has_gpu': __import__('torch').cuda.is_available(),
        'gemini_configured': bool(gemini_api_key),
        'gemini_sdk_available': bool(PROMPT_ENGINEER_GEMINI_AVAILABLE)
    }), 200


@app.route('/api/styles')
def get_styles():
    """Get available styles"""
    styles = [
        'photorealistic',
        'cartoon',
        'watercolor',
        'digital art',
        'oil painting',
        'sketch'
    ]
    return jsonify({'styles': styles}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    gemini_api_key = get_gemini_api_key()
    print("""
    ╔═══════════════════════════════════════╗
    ║     Pitch Visualizer - Web App       ║
    ║  Converting Narratives to Storyboards ║
    ╚═══════════════════════════════════════╝
    """)
    
    print("Starting Flask server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\n⚙️  Configuration:")
    print(f"   - GPU Available: {__import__('torch').cuda.is_available()}")
    print(f"   - Gemini API Configured: {bool(gemini_api_key)}")
    print(f"   - Gemini SDK Available: {bool(PROMPT_ENGINEER_GEMINI_AVAILABLE)}")
    print(f"   - Output Directory: {OUTPUTS_DIR}")
    print("\n💡 Tip: Set GEMINI_API_KEY environment variable to enable LLM prompt engineering")
    print("         Without it, the app will use simple prompt enhancement\n")
    
    # Run on all interfaces to make it accessible
    app.run(debug=True, host='0.0.0.0', port=5000)
