"""
Compression analysis demonstration for transliteration methods.

This script demonstrates how to analyze and compare compression ratios
between different transliteration approaches.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.transliterator import create_transliterator
from utils.compression_calculator import CompressionAnalyzer, calculate_method_compression
from utils.uroman_converter import convert_file_uroman, UROMAN_AVAILABLE


def create_sample_files():
    """Create sample files for compression analysis."""
    
    # Sample texts
    samples = {
        'bo': [
            'འཇིག་རྟེན་གྱི་སངས་རྒྱས་ཆོས་ལུགས་ཀྱི་སེམས་ཀྱིས།',
            'ཐུབ་པའི་བསྟན་པ་རིན་པོ་ཆེ་ལ་བརྟེན་ནས།',
            'སེམས་ཅན་ཐམས་ཅད་ཀྱི་དོན་དུ་ཕན་པའི་ལས།',
            'བདེ་གཤེགས་ཆོས་ཀྱི་འཁོར་ལོ་བསྐོར་བའི་སྐབས།',
            'རྒྱལ་བའི་བཀའ་དྲིན་ལས་བྱུང་བའི་ཤེས་རབ།'
        ],
        'mn': [
            'ᠳᠡᠯᠡᠬᠡᠶ ᠶᠢᠨ ᠪᠤᠳ᠋ᠳ᠋ᠯ ᠶᠢᠨ ᠱᠠ ᠰᠢᠨ ᠰᠡᠳᠬᠢᠯ ᠪᠠᠷ',
            'ᠰᠢᠨ᠎ᠠ ᠪᠤᠷᠬᠠᠨ ᠪᠤᠭᠳᠠ ᠶᠢᠨ ᠰᠦᠷᠭᠠᠭᠤᠯᠢ ᠬᠢᠨ',
            'ᠪᠠᠶᠠᠷ ᠬᠥᠪᠡᠭᠦᠨ ᠦ ᠳᠤᠮᠳᠠᠳᠤ ᠳᠦ ᠲᠦᠰᠢᠯᠠᠬᠤ',
            'ᠡᠷᠬᠡ ᠮᠠᠷᠲᠠᠨ ᠦ ᠨᠣᠮ ᠤᠨ ᠬᠡᠷᠡᠭ ᠢ ᠡᠷᠭᠢᠯᠡᠬᠦ',
            'ᠬᠠᠨ ᠤ ᠪᠠᠶᠠᠷ ᠬᠣᠷᠢᠶ᠎ᠠ ᠨᠤᠲᠤᠭ ᠤᠨ ᠦᠭᠡᠢ'
        ],
        'ug': [
            'دۇنيا بۇددا دىنى ھەققانىيەت ۋە سۆيگۈ بىلەن تولغان',
            'بارلىق جانلىق مەخلۇقاتلارنىڭ بەختىگە يەتكۈزۈش',
            'ئۇچ گۆھەر ئۈچ يۇل ئارقىلىق ئۆگىنىدىغان نۇر',
            'ئۆز-ئۆزىنى ئۆزگەرتىش بىلەن باشقىلارغا پايدا',
            'دانالىق ۋە مېھرىبانلىق بىلەن يول باشلىماق'
        ]
    }
    
    # Create sample directory
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples')
    os.makedirs(sample_dir, exist_ok=True)
    
    created_files = {}
    
    # Create original files
    for lang, texts in samples.items():
        original_file = os.path.join(sample_dir, f'{lang}_original.txt')
        with open(original_file, 'w', encoding='utf-8') as f:
            for text in texts:
                f.write(text + '\n')
        created_files[f'{lang}_original'] = original_file
    
    return created_files, sample_dir


def demo_huffman_compression():
    """Demonstrate Huffman transliteration compression."""
    
    print("="*60)
    print("HUFFMAN TRANSLITERATION COMPRESSION DEMO")
    print("="*60)
    
    # Create sample files
    created_files, sample_dir = create_sample_files()
    
    # Test both encoding methods
    methods = {
        'Basic': create_transliterator('basic'),
        'Optimized': create_transliterator('optimized')
    }
    
    languages = ['bo', 'mn', 'ug']
    
    for method_name, transliterator in methods.items():
        print(f"\n{method_name} Encoding Method:")
        print("-" * 40)
        
        for lang in languages:
            original_file = created_files[f'{lang}_original']
            latin_file = os.path.join(sample_dir, f'{lang}_{method_name.lower()}_latin.txt')
            restored_file = os.path.join(sample_dir, f'{lang}_{method_name.lower()}_restored.txt')
            
            # Read original content
            with open(original_file, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
            
            # Transliterate to Latin
            latin_lines = []
            for line in original_lines:
                latin = transliterator.transliterate_to_latin(line.strip())
                latin_lines.append(latin)
            
            # Save Latin version
            with open(latin_file, 'w', encoding='utf-8') as f:
                for line in latin_lines:
                    f.write(line + '\n')
            
            # Restore from Latin
            restored_lines = []
            for latin_line in latin_lines:
                restored = transliterator.transliterate_from_latin(latin_line)
                restored_lines.append(restored)
            
            # Save restored version
            with open(restored_file, 'w', encoding='utf-8') as f:
                for line in restored_lines:
                    f.write(line + '\n')
            
            # Calculate compression ratios
            original_size = os.path.getsize(original_file)
            latin_size = os.path.getsize(latin_file)
            
            file_ratio = original_size / latin_size if latin_size > 0 else float('inf')
            
            print(f"\nLanguage: {lang.upper()}")
            print(f"  Original file size: {original_size:,} bytes")
            print(f"  Latin file size: {latin_size:,} bytes")
            print(f"  File compression ratio: {file_ratio:.2f}x")
            
            # Check lossless conversion
            original_content = ''.join([line.strip() for line in original_lines])
            restored_content = ''.join(restored_lines)
            
            is_lossless = original_content == restored_content
            print(f"  Lossless conversion: {'✓' if is_lossless else '✗'}")


def demo_token_compression():
    """Demonstrate token-level compression analysis."""
    
    print("\n" + "="*60)
    print("TOKEN COMPRESSION ANALYSIS")
    print("="*60)
    
    # Create a compression analyzer
    try:
        analyzer = CompressionAnalyzer()
        
        # Create sample texts
        test_texts = {
            'Tibetan': 'འཇིག་རྟེན་གྱི་སངས་རྒྱས་ཆོས་ལུགས་ཀྱི་སེམས་ཀྱིས་ཐུབ་པའི་བསྟན་པ།',
            'Mongolian': 'ᠳᠡᠯᠡᠬᠡᠶ ᠶᠢᠨ ᠪᠤᠳ᠋ᠳ᠋ᠯ ᠶᠢᠨ ᠱᠠ ᠰᠢᠨ ᠰᠡᠳᠬᠢᠯ ᠪᠠᠷ ᠪᠠᠶᠠᠷ ᠬᠥᠪᠡᠭᠦᠨ།',
            'Uyghur': 'دۇنيا بۇددا دىنى ھەققانىيەت ۋە سۆيگۈ بىلەن تولغان بارلىق جانلىق مەخلۇقاتلار۔'
        }
        
        transliterator = create_transliterator('optimized')
        
        print(f"{'Language':<12} {'Original':<10} {'Latin':<10} {'Ratio':<8}")
        print("-" * 45)
        
        for lang, text in test_texts.items():
            # Count original tokens
            original_tokens = analyzer.count_tokens(text)
            
            # Transliterate and count
            latin_text = transliterator.transliterate_to_latin(text)
            latin_tokens = analyzer.count_tokens(latin_text)
            
            # Calculate ratio
            token_ratio = original_tokens / latin_tokens if latin_tokens > 0 else float('inf')
            
            print(f"{lang:<12} {original_tokens:<10} {latin_tokens:<10} {token_ratio:<8.2f}x")
        
    except Exception as e:
        print(f"Token analysis requires transformers library: {e}")
        print("Install with: pip install transformers")


def demo_uroman_comparison():
    """Compare with UROMAN if available."""
    
    print("\n" + "="*60)
    print("UROMAN COMPARISON")
    print("="*60)
    
    if not UROMAN_AVAILABLE:
        print("UROMAN not available. Install with: pip install uroman")
        return
    
    # Create sample files
    created_files, sample_dir = create_sample_files()
    
    # Language code mapping for UROMAN
    uroman_codes = {
        'bo': 'bod',
        'mn': 'mon', 
        'ug': 'uig'
    }
    
    transliterator = create_transliterator('optimized')
    
    print(f"{'Language':<10} {'Original (KB)':<12} {'Huffman (KB)':<12} {'UROMAN (KB)':<12}")
    print("-" * 50)
    
    for lang in ['bo', 'mn', 'ug']:
        original_file = created_files[f'{lang}_original']
        huffman_file = os.path.join(sample_dir, f'{lang}_huffman.txt')
        uroman_file = os.path.join(sample_dir, f'{lang}_uroman.txt')
        
        # Create Huffman transliteration
        with open(original_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        huffman_lines = []
        for line in lines:
            latin = transliterator.transliterate_to_latin(line.strip())
            huffman_lines.append(latin)
        
        with open(huffman_file, 'w', encoding='utf-8') as f:
            for line in huffman_lines:
                f.write(line + '\n')
        
        # Create UROMAN transliteration
        try:
            convert_file_uroman(original_file, uroman_file, uroman_codes[lang])
        except Exception as e:
            print(f"Error with UROMAN for {lang}: {e}")
            continue
        
        # Compare file sizes
        original_size = os.path.getsize(original_file) / 1024  # KB
        huffman_size = os.path.getsize(huffman_file) / 1024   # KB
        uroman_size = os.path.getsize(uroman_file) / 1024     # KB
        
        print(f"{lang.upper():<10} {original_size:<12.1f} {huffman_size:<12.1f} {uroman_size:<12.1f}")


def main():
    """Run compression demonstrations."""
    try:
        demo_huffman_compression()
        demo_token_compression()
        demo_uroman_comparison()
        
        print("\n" + "="*60)
        print("COMPRESSION DEMO COMPLETED!")
        print("="*60)
        
    except Exception as e:
        print(f"Error running compression demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()