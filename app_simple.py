"""
Simplified Flask App - Pitch Visualizer
Serves the web interface without image generation to get server running
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
import requests

# Load environment variables
BASE_DIR = os.path.dirname(__file__)
DOTENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=DOTENV_PATH, override=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'outputs')

# Create outputs directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Gemini API
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"


def get_gemini_api_key():
    key = (os.getenv('GEMINI_API_KEY') or '').strip()
    return key.strip('"').strip("'")

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    """Handle storyboard generation requests"""
    data = request.json
    text = data.get('text', '').strip()
    style = data.get('style', 'photorealistic')
    quality = data.get('quality', 'balanced')
    use_api = data.get('use_api', False)
    gemini_api_key = get_gemini_api_key()
    gemini_available = bool(gemini_api_key)
    
    # Validate input
    if not text or len(text) < 20:
        return jsonify({'error': 'Please enter at least 20 characters of narrative text'}), 400
    
    try:
        if use_api:
            if not gemini_available:
                return jsonify({
                    'error': 'Gemini API key not configured. Add GEMINI_API_KEY in pitch-visualizer/.env or uncheck "Use Gemini API".'
                }), 503

            # Use Gemini API REST endpoint to enhance the prompt
            prompt = f"""You are an expert creative director. 
Transform this business narrative into vivid, visual scene descriptions suitable for AI image generation.
Focus on: visual composition, lighting, mood, and key visual elements.
Keep each scene to 2-3 sentences.

Narrative: {text}

Style: {style}
Quality level: {quality}

Provide 3-4 scene descriptions:"""
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            params = {
                "key": gemini_api_key
            }
            
            response = requests.post(GEMINI_API_URL, json=payload, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    enhanced_text = result['candidates'][0]['content']['parts'][0]['text']
                    return jsonify({
                        'success': True,
                        'original': text[:100] + '...' if len(text) > 100 else text,
                        'enhanced': enhanced_text,
                        'style': style,
                        'quality': quality,
                        'message': 'Prompt successfully enhanced with Gemini API'
                    })
                else:
                    return jsonify({'error': 'No response from Gemini API'}), 500
            else:
                error_msg = response.text if response.text else f"HTTP {response.status_code}"
                return jsonify({'error': f'Gemini API error: {error_msg}'}), response.status_code
        else:
            # Return original text without enhancement
            return jsonify({
                'success': True,
                'original': text,
                'enhanced': text,
                'style': style,
                'quality': quality,
                'message': 'Text processed (API enhancement disabled)'
            })
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Gemini API request timeout. Please try again.'}), 504
    except Exception as e:
        return jsonify({'error': f'Error processing with Gemini API: {str(e)}'}), 500

@app.route('/api/status')
def status():
    """Check server status"""
    gemini_api_key = get_gemini_api_key()
    return jsonify({
        'status': 'running', 
        'message': 'Pitch Visualizer Flask server is running',
        'gemini_api': 'available' if gemini_api_key else 'not configured',
        'api_key_set': bool(gemini_api_key)
    })

@app.route('/api/styles')
def get_styles():
    """Return available visual styles"""
    return jsonify({
        'styles': [
            {'id': 'photorealistic', 'name': 'Photorealistic', 'description': 'Realistic, professional quality images'},
            {'id': 'cartoon', 'name': 'Cartoon', 'description': 'Animated, playful cartoon style'},
            {'id': 'watercolor', 'name': 'Watercolor', 'description': 'Artistic watercolor paintings'},
            {'id': 'digital_art', 'name': 'Digital Art', 'description': 'Modern digital illustration'},
            {'id': 'oil_painting', 'name': 'Oil Painting', 'description': 'Classical oil painting style'},
            {'id': 'sketch', 'name': 'Sketch', 'description': 'Hand-drawn pencil sketch'}
        ]
    })

@app.route('/outputs/<filename>')
def download_file(filename):
    """Serve generated files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    gemini_api_key = get_gemini_api_key()
    print("\n" + "="*60)
    print("PITCH VISUALIZER - Flask Server Starting...")
    print("="*60)
    print("\nServer Configuration:")
    print(f"  Web Interface: http://localhost:5000")
    print(f"  Gemini API: {'AVAILABLE' if gemini_api_key else 'NOT CONFIGURED'}")
    print(f"  API Key Status: {'Set' if gemini_api_key else 'Missing'}")
    print("\nNote: Image generation is currently disabled.")
    print("You can test Gemini API for prompt enhancement.")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
