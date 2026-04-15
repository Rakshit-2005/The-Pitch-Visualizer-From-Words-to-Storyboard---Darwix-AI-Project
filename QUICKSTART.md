# ⚡ Quick Start Guide

Get Pitch Visualizer running in 5 minutes!

## Step 1: Install Python (if you don't have it)

Download from [python.org](https://www.python.org) - get version 3.9 or higher.

```bash
python --version  # Should show 3.9+
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First install downloads Stable Diffusion (~4GB). This takes 5-10 minutes on first run only.

On Windows, if you get permission errors:
```bash
pip install --user -r requirements.txt
```

## Step 3: Start the App

```bash
python app.py
```

You'll see:
```
 Pitch Visualizer - Web App
Starting Flask server...
📱 Open your browser and go to: http://localhost:5000
```

## Step 4: Open in Browser

- Copy the URL: `http://localhost:5000`
- Paste into your browser
- You should see the Pitch Visualizer interface

## Step 5: Generate Your First Storyboard

1. **Paste a narrative** (3-5 sentences) in the text box
2. **Pick a style** (photorealistic, cartoon, etc.)
3. **Choose quality** (fast/balanced/high)
4. **Click "Generate Storyboard"**
5. Wait 2-5 minutes (you'll see a loading animation)
6. View your storyboard!

## Example Narrative to Try

```
Sarah managed a sales team but spent hours on manual data entry 
instead of coaching her team. She implemented our CRM platform. 
Her team is now 40% more productive and customer satisfaction improved 25%.
```

---

## 🔑 Optional: Enable Gemini API (Better Prompts)

For even better results, get a free Google Gemini API key:

1. Go to: https://aistudio.google.com/apikey
2. Click "Create API Key" (no credit card!)
3. Copy your key
4. Set environment variable:

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "paste-your-key-here"
python app.py
```

**On Mac/Linux:**
```bash
export GEMINI_API_KEY="paste-your-key-here"
python app.py
```

Then in the web interface, make sure **"Use Gemini API"** is checked.

---

## ⚠️ Common Issues

### "Module not found: torch"
```bash
pip install -r requirements.txt  # Run this again
```

### "CUDA out of memory"
This means your GPU doesn't have enough memory. No worries:
1. Edit `app.py` line 92
2. Change `ImageGenerator(use_cpu=False)` to `ImageGenerator(use_cpu=True)`
3. Restart the app (will be slower but works)

### Generation is very slow
You're using CPU mode (normal, expected). Either:
- Wait it out (grab coffee! ☕)
- Install NVIDIA GPU drivers
- Use fast quality setting instead of high

### Port 5000 already in use
Someone else is using that port. Edit `app.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000 to 5001
```

---

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Try the [CLI mode](cli.py) for command-line usage
- Explore different styles and narrative types
- Customize prompts and generation settings

---

## 🎉 You're ready!

Start generating amazing storyboards. Share them. Impress your audience. Have fun!

**Questions?** Check the README.md troubleshooting section.
