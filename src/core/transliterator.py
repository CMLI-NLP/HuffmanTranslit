"""
Core transliterator module for Huffman-based reversible transliteration.

This module implements the main transliteration functionality for converting
low-resource languages (Tibetan, Mongolian, Uyghur) to Latin representations
and back, ensuring 100% lossless conversion.
"""

import json
from typing import Dict, Optional
from pathlib import Path


class HuffmanTransliterator:
    """
    Huffman-based transliterator for low-resource languages.
    
    Supports reversible transliteration between original scripts and Latin
    representations using frequency-based character encoding.
    """
    
    def __init__(self, mapping_file: str, use_optimized: bool = True):
        """
        Initialize the transliterator with character mappings.
        
        Args:
            mapping_file: Path to JSON file containing character mappings
            use_optimized: Whether to use optimized (way2_code) or basic (latin_code) encoding
        """
        self.char_to_latin: Dict[str, str] = {}
        self.latin_to_char: Dict[str, str] = {}
        self.max_code_length: int = 0
        self.use_optimized = use_optimized
        
        self._load_mappings(mapping_file)
    
    def _load_mappings(self, mapping_file: str) -> None:
        """Load character mappings from JSON file."""
        try:
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mapping_data = json.load(f)
            
            for item in mapping_data:
                if 'char' not in item:
                    continue
                    
                char = item['char']
                code = None
                
                if self.use_optimized:
                    # Use optimized encoding (way2_code)
                    if 'way2_code' in item and item['way2_code'] is not None:
                        code = item['way2_code']
                else:
                    # Use basic encoding (latin_code)
                    if 'latin_code' in item and item['latin_code'] is not None:
                        code = item['latin_code']
                
                if code:
                    self.char_to_latin[char] = code
                    self.latin_to_char[code] = char
                    self.max_code_length = max(self.max_code_length, len(code))
                    
        except Exception as e:
            raise ValueError(f"Failed to load mapping file {mapping_file}: {str(e)}")
    
    def _escape_content(self, text: str) -> str:
        """Escape '@' characters in text to avoid conflicts with delimiters."""
        return text.replace('@', '@@')
    
    def _unescape_content(self, text: str) -> str:
        """Unescape '@@' sequences back to '@' characters."""
        result = []
        i = 0
        while i < len(text):
            if i + 1 < len(text) and text[i:i+2] == '@@':
                result.append('@')
                i += 2
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)
    
    def transliterate_to_latin(self, text: str) -> str:
        """
        Convert original text to Latin representation.
        
        Characters in the mapping table are converted to their Latin codes.
        Unmapped characters are preserved using '@...@' markers with proper escaping.
        
        Args:
            text: Original text to transliterate
            
        Returns:
            Latin representation of the input text
        """
        if not self.char_to_latin:
            return text
            
        result = []
        i = 0
        non_mapped_chars = []
        text_len = len(text)
        
        while i < text_len:
            char = text[i]
            if char in self.char_to_latin:
                # Output any cached unmapped characters first
                if non_mapped_chars:
                    escaped_content = self._escape_content(''.join(non_mapped_chars))
                    result.append('@' + escaped_content + '@')
                    non_mapped_chars = []
                # Output the mapped character
                result.append(self.char_to_latin[char])
            else:
                # Cache unmapped characters
                non_mapped_chars.append(char)
            i += 1
        
        # Output any remaining cached unmapped characters
        if non_mapped_chars:
            escaped_content = self._escape_content(''.join(non_mapped_chars))
            result.append('@' + escaped_content + '@')
        
        return ''.join(result)
    
    def transliterate_from_latin(self, latin_text: str) -> str:
        """
        Convert Latin representation back to original text.
        
        Uses greedy matching to find the longest possible Latin codes.
        Handles '@...@' markers for preserved unmapped characters.
        
        Args:
            latin_text: Latin representation to convert back
            
        Returns:
            Original text restored from Latin representation
        """
        result = []
        i = 0
        text_len = len(latin_text)
        
        while i < text_len:
            if latin_text[i] == '@':
                # Handle preserved unmapped content
                i += 1
                non_mapped_content = []
                
                while i < text_len:
                    # Handle escaped '@' characters
                    if i + 1 < text_len and latin_text[i:i+2] == '@@':
                        non_mapped_content.append('@')
                        i += 2
                    elif latin_text[i] == '@':
                        i += 1
                        break
                    else:
                        non_mapped_content.append(latin_text[i])
                        i += 1
                
                result.append(''.join(non_mapped_content))
            
            else:
                # Try to match Latin codes greedily (longest first)
                found = False
                for length in range(self.max_code_length, 0, -1):
                    if i + length <= text_len:
                        potential_code = latin_text[i:i + length]
                        if potential_code in self.latin_to_char:
                            result.append(self.latin_to_char[potential_code])
                            i += length
                            found = True
                            break
                if not found:
                    # Skip unrecognized character
                    i += 1
        
        return ''.join(result)
    
    def is_lossless(self, original_text: str) -> bool:
        """
        Check if the transliteration is lossless for given text.
        
        Args:
            original_text: Original text to test
            
        Returns:
            True if transliteration is lossless, False otherwise
        """
        latin = self.transliterate_to_latin(original_text)
        restored = self.transliterate_from_latin(latin)
        return original_text == restored
    
    def get_coverage_stats(self, text: str) -> Dict[str, int]:
        """
        Get statistics about character coverage in the mapping.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with mapped_chars, unmapped_chars, total_chars counts
        """
        mapped_chars = 0
        unmapped_chars = 0
        
        for char in text:
            if char in self.char_to_latin:
                mapped_chars += 1
            else:
                unmapped_chars += 1
        
        return {
            'mapped_chars': mapped_chars,
            'unmapped_chars': unmapped_chars,
            'total_chars': len(text),
            'coverage_ratio': mapped_chars / len(text) if text else 0.0
        }


def create_transliterator(mapping_type: str = "optimized") -> HuffmanTransliterator:
    """
    Factory function to create a transliterator with default mappings.
    
    Args:
        mapping_type: Either "basic" or "optimized"
        
    Returns:
        Configured HuffmanTransliterator instance
    """
    base_dir = Path(__file__).parent.parent.parent
    
    if mapping_type == "basic":
        mapping_file = base_dir / "data" / "character_mappings" / "basic_mapping.json"
        use_optimized = False
    elif mapping_type == "optimized":
        mapping_file = base_dir / "data" / "character_mappings" / "optimized_mapping.json"
        use_optimized = True
    else:
        raise ValueError(f"Unknown mapping type: {mapping_type}")
    
    return HuffmanTransliterator(str(mapping_file), use_optimized=use_optimized)