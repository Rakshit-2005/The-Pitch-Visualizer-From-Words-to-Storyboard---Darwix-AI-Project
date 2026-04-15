"""
Prompt Engineering Module
Enhances narrative sentences into visually rich image prompts using Gemini API
"""

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except Exception as e:
    print(f"Warning: Gemini API not available: {e}")
    GEMINI_AVAILABLE = False

import time
from typing import List, Optional


class PromptEngineer:
    """Handles prompt enhancement using Google Gemini API"""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini API
        
        Args:
            api_key (str): Google Gemini API key
        """
        if not GEMINI_AVAILABLE:
            raise Exception("Gemini API is not available")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.rate_limit_delay = 1  # Seconds between requests
    
    def enhance_prompt(self, sentence: str, style: str = "photorealistic") -> str:
        """
        Transform a narrative sentence into a detailed image prompt
        
        Args:
            sentence (str): Original narrative sentence
            style (str): Visual style (photorealistic, cartoon, watercolor, digital art)
        
        Returns:
            str: Enhanced visual prompt
        """
        style_descriptions = {
            "photorealistic": "photorealistic, high detail, cinematic lighting, professional photography",
            "cartoon": "animated style, bright colors, fun and playful, cartoon aesthetic",
            "watercolor": "watercolor painting, soft edges, artistic, delicate brushstrokes",
            "digital art": "digital art style, vibrant colors, modern aesthetic, high quality",
            "oil painting": "oil painting style, classical art, detailed and textured",
            "sketch": "pencil sketch, artistic lines, minimalist, refined details"
        }
        
        style_prompt = style_descriptions.get(style, style_descriptions["photorealistic"])
        
        prompt = f"""Transform this narrative sentence into a detailed, visually rich image prompt 
        for an AI image generator. Make it cinematic, descriptive, and emotionally evocative.
        
        Style: {style_prompt}
        
        Original sentence: "{sentence}"
        
        Create a detailed visual prompt (2-3 sentences) that captures the essence and emotion 
        of the original text while being highly descriptive for image generation. 
        Focus on visual elements, emotions, lighting, and composition.
        
        Enhanced visual prompt:"""
        
        try:
            response = self.model.generate_content(prompt)
            enhanced = response.text.strip()
            
            # Add style description to the end
            if style not in enhanced.lower():
                enhanced += f", {style_prompt}"
            
            return enhanced
        
        except Exception as e:
            print(f"Error enhancing prompt: {str(e)}")
            # Fallback: return original with style
            return f"{sentence}. Visual style: {style_prompt}"
    
    def enhance_prompts_batch(self, sentences: List[str], style: str = "photorealistic") -> List[str]:
        """
        Enhance multiple sentences to prompts
        
        Args:
            sentences (List[str]): List of narrative sentences
            style (str): Visual style to apply
        
        Returns:
            List[str]: List of enhanced prompts
        """
        enhanced_prompts = []
        
        for i, sentence in enumerate(sentences):
            print(f"Enhancing prompt {i + 1}/{len(sentences)}...")
            
            enhanced = self.enhance_prompt(sentence, style)
            enhanced_prompts.append(enhanced)
            
            # Rate limiting to avoid API overload
            if i < len(sentences) - 1:
                time.sleep(self.rate_limit_delay)
        
        return enhanced_prompts


def create_simple_prompt(sentence: str, style: str = "photorealistic") -> str:
    """
    Fallback: Create enhanced prompt without API (for testing)
    
    Args:
        sentence (str): Original sentence
        style (str): Visual style
    
    Returns:
        str: Enhanced prompt
    """
    style_keywords = {
        "photorealistic": "photorealistic, high detail, cinematic lighting, professional",
        "cartoon": "animated, bright colors, cartoon style, playful",
        "watercolor": "watercolor painting, soft edges, artistic",
        "digital art": "digital art, vibrant, modern, high quality",
        "oil painting": "oil painting, classical, detailed",
        "sketch": "pencil sketch, artistic, minimalist"
    }
    
    keywords = style_keywords.get(style, style_keywords["photorealistic"])
    
    # Simple enhancement: add descriptive elements
    enhanced = f"{sentence} Visual style: {keywords}, attention to emotion and atmosphere. "
    
    return enhanced


if __name__ == "__main__":
    # Example usage (requires API key)
    api_key = "YOUR_GEMINI_API_KEY"
    
    sentences = [
        "Sarah was struggling with her sales team's manual processes.",
        "She discovered our automation platform.",
        "Now her team closes deals 40% faster."
    ]
    
    # Uncomment to test with actual API
    # engineer = PromptEngineer(api_key)
    # enhanced = engineer.enhance_prompts_batch(sentences, style="photorealistic")
    # for orig, enh in zip(sentences, enhanced):
    #     print(f"Original: {orig}")
    #     print(f"Enhanced: {enh}\n")
    
    # Or use fallback
    for sentence in sentences:
        enhanced = create_simple_prompt(sentence)
        print(f"Original: {sentence}")
        print(f"Enhanced: {enhanced}\n")
