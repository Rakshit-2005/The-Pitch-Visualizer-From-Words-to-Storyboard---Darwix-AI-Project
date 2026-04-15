"""
Text Segmentation Module
Breaks down narrative text into logical scenes for image generation
"""

import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


def segment_text(text, min_segments=3):
    """
    Segment text into logical scenes/sentences
    
    Args:
        text (str): Input narrative text
        min_segments (int): Minimum number of segments required
    
    Returns:
        list: List of text segments (sentences)
    """
    # Clean up whitespace
    text = text.strip()
    
    # Tokenize into sentences
    sentences = sent_tokenize(text)
    
    # Remove empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # If we have fewer than min_segments, keep them as is
    if len(sentences) < min_segments:
        print(f"Warning: Only {len(sentences)} sentences found. Minimum recommended is {min_segments}.")
        return sentences
    
    return sentences


def get_key_phrases(text, num_phrases=3):
    """
    Extract key phrases from text (alternative to sentence segmentation)
    
    Args:
        text (str): Input narrative text
        num_phrases (int): Number of key phrases to extract
    
    Returns:
        list: List of key phrases
    """
    sentences = sent_tokenize(text)
    
    # Simple heuristic: use sentences as phrases, take every nth sentence
    if len(sentences) <= num_phrases:
        return sentences
    
    step = len(sentences) // num_phrases
    return [sentences[i * step] for i in range(num_phrases)]


def validate_text_input(text, min_length=20):
    """
    Validate user input text
    
    Args:
        text (str): Input text to validate
        min_length (int): Minimum text length
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not text:
        return False, "Text cannot be empty"
    
    if len(text.strip()) < min_length:
        return False, f"Text must be at least {min_length} characters long"
    
    # Check if text has at least 3 sentences
    sentences = sent_tokenize(text)
    if len(sentences) < 3:
        return False, "Text must contain at least 3 sentences"
    
    return True, "Valid"


if __name__ == "__main__":
    # Example usage
    sample_text = """
    Sarah was struggling with her sales team's manual processes. 
    She discovered our automation platform. 
    Now her team closes deals 40% faster.
    """
    
    segments = segment_text(sample_text)
    print("Segments:")
    for i, seg in enumerate(segments, 1):
        print(f"{i}. {seg}")
