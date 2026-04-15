"""
Storyboard Generator Module
Creates HTML storyboards from images and captions
"""

from typing import List, Tuple
import os
from datetime import datetime


class StoryboardGenerator:
    """Generate HTML storyboard from images and text"""
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize storyboard generator
        
        Args:
            output_dir (str): Directory where storyboards will be saved
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_html(self, 
                     image_paths: List[str],
                     captions: List[str],
                     title: str = "Pitch Visualizer Storyboard",
                     style: str = "photorealistic") -> str:
        """
        Generate HTML storyboard
        
        Args:
            image_paths (List[str]): List of image file paths
            captions (List[str]): List of caption texts
            title (str): Storyboard title
            style (str): Visual style used
        
        Returns:
            str: HTML content
        """
        if len(image_paths) != len(captions):
            raise ValueError("Number of images must match number of captions")
        
        # Create panels HTML
        panels_html = ""
        for i, (img_path, caption) in enumerate(zip(image_paths, captions), 1):
            # Convert absolute path to relative for HTML
            img_name = os.path.basename(img_path)
            
            panels_html += f"""
            <div class="panel" data-panel="{i}">
                <div class="panel-number">Scene {i}</div>
                <img src="{img_name}" class="panel-image" alt="Scene {i}" loading="lazy">
                <div class="panel-caption">
                    <p>{caption}</p>
                </div>
            </div>
            """
        
        # Generate full HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 50px;
            animation: fadeIn 0.8s ease-in;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        
        .style-tag {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
            backdrop-filter: blur(10px);
        }}
        
        .storyboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }}
        
        .panel {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: slideUp 0.6s ease-out;
            animation-fill-mode: both;
        }}
        
        .panel:nth-child(1) {{ animation-delay: 0s; }}
        .panel:nth-child(2) {{ animation-delay: 0.2s; }}
        .panel:nth-child(3) {{ animation-delay: 0.4s; }}
        .panel:nth-child(4) {{ animation-delay: 0.6s; }}
        .panel:nth-child(5) {{ animation-delay: 0.8s; }}
        
        .panel:hover {{
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }}
        
        .panel-number {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px;
            font-weight: bold;
            text-align: center;
            font-size: 0.9em;
        }}
        
        .panel-image {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            display: block;
        }}
        
        .panel-caption {{
            padding: 20px;
            background: #f8f9fa;
        }}
        
        .panel-caption p {{
            font-size: 1em;
            line-height: 1.6;
            color: #333;
            font-weight: 500;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            padding-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.2);
            animation: fadeIn 1s ease-in 0.8s both;
        }}
        
        .footer p {{
            opacity: 0.8;
            font-size: 0.9em;
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .storyboard {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .panel-image {{
                height: 250px;
            }}
        }}
        
        .download-btn {{
            display: inline-block;
            margin-top: 10px;
            padding: 10px 20px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        
        .download-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ {title}</h1>
            <p>Your narrative brought to life through AI-generated imagery</p>
            <div class="style-tag">Style: <strong>{style.title()}</strong></div>
        </div>
        
        <div class="storyboard">
            {panels_html}
        </div>
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Powered by Stable Diffusion & Gemini API</p>
        </div>
    </div>
</body>
</html>
"""
        return html_content
    
    def save_html(self, html_content: str, filename: str = "storyboard.html") -> str:
        """
        Save HTML to file
        
        Args:
            html_content (str): HTML content
            filename (str): Output filename
        
        Returns:
            str: Full path to saved file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Storyboard saved to: {filepath}")
        return filepath
    
    def create_storyboard(self,
                         image_paths: List[str],
                         captions: List[str],
                         title: str = "Pitch Visualizer",
                         style: str = "photorealistic",
                         filename: str = "storyboard.html") -> str:
        """
        Create and save complete storyboard
        
        Args:
            image_paths (List[str]): List of image paths
            captions (List[str]): List of captions
            title (str): Storyboard title
            style (str): Visual style
            filename (str): Output filename
        
        Returns:
            str: Path to saved HTML file
        """
        html = self.generate_html(image_paths, captions, title, style)
        return self.save_html(html, filename)


if __name__ == "__main__":
    # Example usage
    generator = StoryboardGenerator(output_dir="outputs")
    
    # Mock image paths and captions
    image_paths = [
        "outputs/storyboard_scene_01.png",
        "outputs/storyboard_scene_02.png",
        "outputs/storyboard_scene_03.png",
    ]
    
    captions = [
        "Sarah was struggling with her sales team's manual processes.",
        "She discovered our automation platform.",
        "Now her team closes deals 40% faster.",
    ]
    
    # Uncomment to test
    # filepath = generator.create_storyboard(image_paths, captions, "Sales Success Story")
    # print(f"Storyboard created at: {filepath}")
