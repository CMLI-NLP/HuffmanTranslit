"""
HuffmanTranslit: Reversible Transliteration for Low-Resource Languages

This package provides a Huffman coding-based approach for reversible
transliteration of low-resource languages (Tibetan, Mongolian, Uyghur).

Main Features:
- 100% lossless transliteration
- Significant compression ratios
- Multi-strategy encoding support
- Easy integration with existing NLP pipelines

Quick Start:
    >>> from huffmantranslit import create_transliterator
    >>> transliterator = create_transliterator('optimized')
    >>> latin = transliterator.transliterate_to_latin("འཇིག་རྟེན།")
    >>> original = transliterator.transliterate_from_latin(latin)
"""

__version__ = "1.0.0"
__author__ = "Wenhao Zhuang, Yuan Sun, Xiaobing Zhao"
__email__ = "sunyuan@muc.edu.cn"

# Import main classes and functions for easy access
from .core.transliterator import HuffmanTransliterator, create_transliterator
from .utils.char_analyzer import CharacterAnalyzer
from .utils.compression_calculator import CompressionAnalyzer

# Define what gets imported with "from huffmantranslit import *"
__all__ = [
    "HuffmanTransliterator",
    "create_transliterator", 
    "CharacterAnalyzer",
    "CompressionAnalyzer",
]