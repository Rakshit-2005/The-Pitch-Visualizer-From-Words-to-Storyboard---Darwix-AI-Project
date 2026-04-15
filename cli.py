#!/usr/bin/env python
"""
Pitch Visualizer - Command Line Interface
Run without web server for testing and development
"""

import os
import sys
import argparse
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from text_processor import segment_text, validate_text_input
from prompt_engineer import PromptEngineer, create_simple_prompt
from image_generator import ImageGenerator, get_generation_params
from storyboard_generator import StoryboardGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Pitch Visualizer - Convert narratives to AI storyboards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic usage with simple prompt enhancement
  python cli.py "Your narrative text here"
  
  # With Gemini API and custom style
  python cli.py "Your narrative" --api --style watercolor
  
  # CPU mode (slow but no GPU needed)
  python cli.py "Your narrative" --cpu
  
  # High quality output
  python cli.py "Your narrative" --quality high
        '''
    )
    
    parser.add_argument(
        'text',
        help='Narrative text (minimum 3 sentences)'
    )
    
    parser.add_argument(
        '--style',
        choices=['photorealistic', 'cartoon', 'watercolor', 'digital art', 'oil painting', 'sketch'],
        default='photorealistic',
        help='Visual style (default: photorealistic)'
    )
    
    parser.add_argument(
        '--quality',
        choices=['fast', 'balanced', 'high'],
        default='balanced',
        help='Generation quality/speed (default: balanced)'
    )
    
    parser.add_argument(
        '--api',
        action='store_true',
        help='Use Gemini API for prompt engineering (requires GEMINI_API_KEY)'
    )
    
    parser.add_argument(
        '--cpu',
        action='store_true',
        help='Use CPU for image generation (slower, no GPU needed)'
    )
    
    parser.add_argument(
        '--output',
        default='outputs',
        help='Output directory (default: outputs)'
    )
    
    args = parser.parse_args()
    
    print("""
    ╔═══════════════════════════════════════╗
    ║     Pitch Visualizer - CLI Mode       ║
    ║  Converting Narratives to Storyboards ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Validate input
    print("[1/5] Validating input...")
    is_valid, error_msg = validate_text_input(args.text)
    if not is_valid:
        print(f"❌ Error: {error_msg}")
        sys.exit(1)
    
    # Segment text
    print("[2/5] Segmenting narrative...")
    segments = segment_text(args.text)
    print(f"✓ Found {len(segments)} scenes:")
    for i, seg in enumerate(segments, 1):
        print(f"   {i}. {seg[:70]}...")
    
    # Engineer prompts
    print(f"\n[3/5] Engineering prompts (style: {args.style})...")
    if args.api:
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            print("❌ Error: GEMINI_API_KEY not set")
            print("   Set it with: export GEMINI_API_KEY=your-key")
            sys.exit(1)
        
        engineer = PromptEngineer(api_key)
        prompts = engineer.enhance_prompts_batch(segments, args.style)
    else:
        prompts = [create_simple_prompt(seg, args.style) for seg in segments]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"✓ Prompt {i}: {prompt[:80]}...")
    
    # Generate images
    print(f"\n[4/5] Generating images (this may take 1-5 minutes)...")
    print(f"   Using: {'GPU' if not args.cpu else 'CPU'}")
    print(f"   Quality: {args.quality}")
    
    generator = ImageGenerator(use_cpu=args.cpu)
    gen_params = get_generation_params(args.quality)
    
    image_results = generator.generate_images_batch(
        prompts,
        output_dir=args.output,
        **gen_params
    )
    generator.cleanup()
    
    image_paths = [path for path, _ in image_results if path is not None]
    if not image_paths:
        print("❌ Error: Failed to generate any images")
        sys.exit(1)
    
    print(f"✓ Generated {len(image_paths)} images")
    
    # Create storyboard
    print(f"\n[5/5] Creating storyboard...")
    storyboard_gen = StoryboardGenerator(args.output)
    
    html_path = storyboard_gen.create_storyboard(
        image_paths,
        segments[:len(image_paths)],
        title="Pitch Visualizer Storyboard",
        style=args.style,
        filename="storyboard.html"
    )
    
    print(f"\n✨ Success! Storyboard created:")
    print(f"   📁 {html_path}")
    print(f"\n🚀 Open in browser to view: file://{os.path.abspath(html_path)}")
    print(f"\n📊 Summary:")
    print(f"   - Scenes: {len(segments)}")
    print(f"   - Images: {len(image_paths)}")
    print(f"   - Style: {args.style}")
    print(f"   - Quality: {args.quality}")


if __name__ == '__main__':
    main()
