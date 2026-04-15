# 📁 Project Structure & File Guide

## Complete File Listing

```
pitch-visualizer/
├── app.py                          # Main Flask web application
├── text_processor.py              # Text segmentation & validation
├── prompt_engineer.py             # LLM-powered prompt enhancement (Gemini)
├── image_generator.py             # Stable Diffusion image generation
├── storyboard_generator.py        # HTML storyboard creation
├── cli.py                         # Command-line interface
├── requirements.txt               # Python dependencies
├── setup.bat                      # Windows setup script
├── setup.sh                       # Mac/Linux setup script
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── README.md                      # Full documentation
├── QUICKSTART.md                  # Quick start guide (read this first!)
├── PROJECT_STRUCTURE.md           # This file
├── templates/
│   └── index.html                # Web UI (Flask template)
├── static/                        # CSS/JS assets (optional, for custom styling)
└── outputs/                       # Generated images & storyboards (created at runtime)
```

---

## 📄 File Descriptions

### Core Application Files

#### `app.py` (Main Application)
**Purpose**: Flask web application server
**Key Features**:
- `/` - Home page with UI
- `/api/generate` - Main API endpoint for storyboard generation
- `/api/status` - Check if API is online and GPU available
- `/api/styles` - Get list of available styles
- Error handling and CORS support

**Run with**: `python app.py`

---

#### `text_processor.py` (Text Processing)
**Purpose**: Parse and segment narrative text
**Functions**:
- `segment_text()` - Split text into sentences (3+ minimum)
- `validate_text_input()` - Validate user input
- `get_key_phrases()` - Extract important phrases

**No external API calls** - all local processing

---

#### `prompt_engineer.py` (Prompt Enhancement)
**Purpose**: Transform sentences into visual image prompts
**Classes**:
- `PromptEngineer` - Uses Google Gemini API for intelligent enhancement
- `create_simple_prompt()` - Fallback method without API

**API Used**: Google Gemini 2.0 Flash (free tier)

---

#### `image_generator.py` (Image Generation)
**Purpose**: Generate images from prompts using Stable Diffusion
**Classes**:
- `ImageGenerator` - Manages Stable Diffusion pipeline
  - Supports GPU and CPU modes
  - Memory optimizations included
  - Batch processing support

**Model**: `runwayml/stable-diffusion-v1-5` (~4GB)

---

#### `storyboard_generator.py` (HTML Assembly)
**Purpose**: Create interactive HTML storyboards
**Classes**:
- `StoryboardGenerator` - Generates styled HTML with animations
  - Responsive design
  - Mobile-friendly
  - Beautiful CSS animations

**Output**: Standalone HTML file (can be shared)

---

### User Interface

#### `templates/index.html` (Web UI)
**Purpose**: Interactive web interface
**Features**:
- Text input area
- Style selector (6 options)
- Quality selector
- API toggle
- Real-time generation status
- Results viewer

**Styling**: Modern gradient design with animations, fully responsive

---

### Setup & Configuration

#### `requirements.txt`
**Purpose**: Python package dependencies
**Contains**:
- Flask 3.0.0
- PyTorch 2.1.2 (image generation)
- Transformers 4.35.2 (NLP)
- Diffusers 0.25.0 (Stable Diffusion)
- Google Generative AI 0.3.0 (Gemini)
- NLTK 3.8.1 (text processing)
- And more...

**Install with**: `pip install -r requirements.txt`

---

#### `setup.bat` (Windows Setup)
**Purpose**: Automated setup for Windows users
**Does**:
1. Checks Python installation
2. Creates virtual environment
3. Activates virtual environment
4. Installs all dependencies

**Run with**: `setup.bat` (double-click)

---

#### `setup.sh` (Mac/Linux Setup)
**Purpose**: Automated setup for Mac/Linux users
**Does**: Same as setup.bat for Unix systems

**Run with**: `bash setup.sh`

---

#### `.env.example`
**Purpose**: Template for environment variables
**Contains**:
- GEMINI_API_KEY (optional, for better prompts)
- OUTPUT_DIR (where to save files)
- FLASK settings

**Usage**: Copy to `.env` and fill in your values

---

#### `.gitignore`
**Purpose**: Git configuration (if using version control)
**Ignores**:
- Python cache files
- Virtual environments
- Generated outputs
- IDE config files
- System files

---

### Documentation

#### `README.md` (Full Documentation)
**Contains**:
- Project overview
- Installation instructions
- Configuration guide
- Usage examples
- Architecture explanation
- Customization guide
- API reference
- Troubleshooting
- Deployment instructions
- Future enhancements

**Read This**: Before asking questions

---

#### `QUICKSTART.md` (Quick Start Guide)
**Contains**:
- 5-minute setup guide
- First storyboard creation
- Common issues & fixes

**Read This**: To get started immediately

---

#### `PROJECT_STRUCTURE.md` (This File)
**Purpose**: Detailed explanation of every file and folder

---

### Runtime Folders (Created Automatically)

#### `outputs/`
**Purpose**: Store generated images and storyboards
**Contains**:
- `storyboard_scene_01.png` - images
- `storyboard_scene_02.png` - (one per scene)
- `storyboard_YYYY-MM-DD_HH-MM-SS.html` - storyboard files

**Created**: When you generate your first storyboard
**Size**: ~5MB+ per storyboard (depends on image resolution)

---

#### `venv/` (Virtual Environment)
**Purpose**: Isolated Python environment
**Created**: By `setup.bat`/`setup.sh` or `python -m venv venv`
**Size**: ~500MB (first time only)

**Activate**:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

---

### Optional Folders

#### `static/`
**Purpose**: Store custom CSS/JavaScript (optional)
**Currently**: Empty (basic styling is in `index.html`)
**For**: Advanced customization

---

## 🔄 Data Flow

```
User Input (Web Form)
    ↓
app.py (Flask route handler)
    ↓
text_processor.py (segment narrative)
    ↓
prompt_engineer.py (enhance prompts with Gemini)
    ↓
image_generator.py (generate images with Stable Diffusion)
    ↓
storyboard_generator.py (create HTML)
    ↓
outputs/ folder (save files)
    ↓
Web browser (display results)
```

---

## 📊 File Dependencies

```
app.py
├── depends on: text_processor.py
├── depends on: prompt_engineer.py
├── depends on: image_generator.py
├── depends on: storyboard_generator.py
└── serves: templates/index.html

cli.py
├── depends on: text_processor.py
├── depends on: prompt_engineer.py
├── depends on: image_generator.py
└── depends on: storyboard_generator.py
```

---

## 🚀 How to Run

### Option 1: Web Interface (Recommended)
```bash
python app.py
# Open http://localhost:5000
```

### Option 2: Command Line
```bash
python cli.py "Your narrative text here"
```

### Option 3: Automated Setup (First Time)
```bash
# Windows
setup.bat

# Mac/Linux
bash setup.sh
```

---

## 📝 File Size Reference

| File | Size | Notes |
|------|------|-------|
| app.py | ~5 KB | Main application |
| text_processor.py | ~3 KB | Text processing |
| prompt_engineer.py | ~4 KB | Prompt enhancement |
| image_generator.py | ~6 KB | Image generation |
| storyboard_generator.py | ~5 KB | HTML assembly |
| templates/index.html | ~10 KB | Web UI |
| requirements.txt | <1 KB | Dependencies list |
| **Total Python Code** | **~33 KB** | Very lightweight |
| **Models (at runtime)** | **~4.3 GB** | Downloaded on first use |
| **Generated Storyboard** | **~3-5 MB** | Per storyboard |

---

## 💾 Disk Space Needed

| Phase | Space | Notes |
|-------|-------|-------|
| Install dependencies | 1-2 GB | One-time |
| Stable Diffusion model | 4 GB | One-time, downloaded on first image |
| Generated storyboards | 3-5 MB each | Per storyboard |
| **Total for 10 storyboards** | **4.5-4.8 GB** | After initial setup |

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] All Python files present (app.py, etc.)
- [ ] `requirements.txt` installed
- [ ] Virtual environment created (if using)
- [ ] Flask server starts without errors
- [ ] Web UI loads at localhost:5000
- [ ] Can generate a test storyboard
- [ ] Images save to `outputs/`
- [ ] HTML storyboard creates successfully

---

## 🔧 Customization Points

If you want to modify the project:

| Want to change | Edit file | What to change |
|---|---|---|
| Web UI colors/styling | `templates/index.html` | CSS section |
| Image generation speed | `app.py` | `steps` parameter |
| Styles available | `prompt_engineer.py` | `style_descriptions` dict |
| Text segmentation method | `text_processor.py` | `segment_text()` function |
| API keys/config | `.env` or `app.py` | Environment variables |
| Port number | `app.py` | `app.run(port=5000)` |

---

## 📚 Example Workflows

### Workflow 1: Generate One Storyboard
```
1. Run: python app.py
2. Open: http://localhost:5000
3. Paste narrative
4. Click "Generate"
5. View results
6. Download/share storyboard.html
```

### Workflow 2: Batch Processing (CLI)
```
python cli.py "Story 1 here"
python cli.py "Story 2 here" --api --style watercolor
python cli.py "Story 3 here" --quality high --cpu
```

### Workflow 3: Development/Testing
```
1. Edit source files (e.g., prompt_engineer.py)
2. Restart Flask app
3. Test changes in web UI
4. Repeat until satisfied
```

---

## 🎓 Learning Path

To understand the project:

1. **Start Here**: Read `QUICKSTART.md` (5 min)
2. **Front-End**: Look at `templates/index.html` (10 min)
3. **Back-End Flow**: Read top comments in `app.py` (5 min)
4. **Core Logic**: Study each module:
   - `text_processor.py` (2 min)
   - `prompt_engineer.py` (3 min)
   - `image_generator.py` (3 min)
   - `storyboard_generator.py` (2 min)
5. **Deep Dive**: Read full `README.md` (15 min)

**Total time**: ~45 minutes to fully understand the project

---

**That's it! You now understand the complete project structure.** 🎉
