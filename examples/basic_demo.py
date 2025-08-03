"""
Basic demonstration of Huffman-based transliteration.

This script shows how to use the HuffmanTransliterator for basic
transliteration tasks with different character mappings.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.transliterator import HuffmanTransliterator, create_transliterator


def demo_basic_transliteration():
    """Demonstrate basic transliteration functionality."""
    
    print("="*60)
    print("HUFFMAN TRANSLITERATION DEMO")
    print("="*60)
    
    # Sample texts in different languages
    samples = {
        'Tibetan': 'འཇིག་རྟེན་གྱི་སངས་རྒྱས་ཆོས་ལུགས་ཀྱི་སེམས་can།',
        'Mongolian': 'ᠳᠡᠯᠡᠬᠡᠶ ᠶᠢᠨ ᠪᠤᠳ᠋ᠳ᠋ᠯ ᠶᠢᠨ ᠱᠠ world ᠰᠢᠨ།',
        'Uyghur': 'دۇنيا بۇددا دىنىninghouse ھەققانىيەت।',
        'Mixed': 'འཇིག་རྟེན་peace and loveཞི་བདེ།'
    }
    
    # Test both basic and optimized transliterators
    transliterators = {
        'Basic Encoding': create_transliterator('basic'),
        'Optimized Encoding': create_transliterator('optimized')
    }
    
    for method_name, transliterator in transliterators.items():
        print(f"\n{method_name}:")
        print("-" * 40)
        
        for lang, text in samples.items():
            print(f"\n{lang} Original:")
            print(f"  {text}")
            
            # Transliterate to Latin
            latin = transliterator.transliterate_to_latin(text)
            print(f"{lang} Latin:")
            print(f"  {latin}")
            
            # Transliterate back to original
            restored = transliterator.transliterate_from_latin(latin)
            print(f"{lang} Restored:")
            print(f"  {restored}")
            
            # Check if lossless
            is_lossless = transliterator.is_lossless(text)
            status = "✓ LOSSLESS" if is_lossless else "✗ LOSSY"
            print(f"  Status: {status}")
            
            # Get coverage statistics
            stats = transliterator.get_coverage_stats(text)
            print(f"  Coverage: {stats['mapped_chars']}/{stats['total_chars']} "
                  f"({stats['coverage_ratio']:.1%})")


def demo_file_processing():
    """Demonstrate processing text files."""
    
    print("\n" + "="*60)
    print("FILE PROCESSING DEMO")
    print("="*60)
    
    # Create a sample file
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples')
    os.makedirs(sample_dir, exist_ok=True)
    
    sample_file = os.path.join(sample_dir, 'demo_input.txt')
    output_file = os.path.join(sample_dir, 'demo_output.txt')
    restored_file = os.path.join(sample_dir, 'demo_restored.txt')
    
    # Write sample content
    sample_lines = [
        'འཇིག་རྟེན་གྱི་སངས་རྒྱས་ཆོས་ལུགས།',
        'ᠳᠡᠯᠡᠬᠡᠶ ᠶᠢᠨ ᠪᠤᠳ᠋ᠳ᠋ᠯ ᠶᠢᠨ ᠱᠠ།',
        'دۇنيا بۇددا دىنى ھەققانىيەت।',
        'Mixed text with English and ཞི་བདེ'
    ]
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        for line in sample_lines:
            f.write(line + '\n')
    
    print(f"Created sample file: {sample_file}")
    
    # Process the file
    transliterator = create_transliterator('optimized')
    
    # Read and transliterate
    transliterated_lines = []
    with open(sample_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                latin = transliterator.transliterate_to_latin(line)
                transliterated_lines.append(latin)
    
    # Write transliterated file
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in transliterated_lines:
            f.write(line + '\n')
    
    print(f"Transliterated file saved: {output_file}")
    
    # Restore and save
    restored_lines = []
    for latin_line in transliterated_lines:
        restored = transliterator.transliterate_from_latin(latin_line)
        restored_lines.append(restored)
    
    with open(restored_file, 'w', encoding='utf-8') as f:
        for line in restored_lines:
            f.write(line + '\n')
    
    print(f"Restored file saved: {restored_file}")
    
    # Verify lossless conversion
    original_content = '\n'.join(sample_lines)
    restored_content = '\n'.join(restored_lines)
    
    if original_content == restored_content:
        print("✓ File processing is LOSSLESS")
    else:
        print("✗ File processing is LOSSY")
        print(f"Original length: {len(original_content)}")
        print(f"Restored length: {len(restored_content)}")


def demo_coverage_analysis():
    """Demonstrate character coverage analysis."""
    
    print("\n" + "="*60)
    print("CHARACTER COVERAGE ANALYSIS")
    print("="*60)
    
    # Test texts with different character sets
    test_texts = {
        'Pure Tibetan': 'འཇིག་རྟེན་གྱི་སངས་རྒྱས་ཆོས་ལུགས་ཀྱི་སེམས་ཀྱིས།',
        'Pure Mongolian': 'ᠳᠡᠯᠡᠬᠡᠶ ᠶᠢᠨ ᠪᠤᠳ᠋ᠳ᠋ᠯ ᠶᠢᠨ ᠱᠠ ᠰᠢᠨ།',
        'Mixed Script': 'འཇིག་རྟེན་peace and loveཞི་བདེ།',
        'With Numbers': 'Year 2024 - འཇིག་རྟེན་གྱི། 123 456',
        'With Emojis': 'Hello 😀 འཇིག་རྟེན་ 🌍 world!'
    }
    
    transliterator = create_transliterator('optimized')
    
    for desc, text in test_texts.items():
        print(f"\n{desc}:")
        print(f"  Text: {text}")
        
        stats = transliterator.get_coverage_stats(text)
        print(f"  Total chars: {stats['total_chars']}")
        print(f"  Mapped chars: {stats['mapped_chars']}")
        print(f"  Unmapped chars: {stats['unmapped_chars']}")
        print(f"  Coverage: {stats['coverage_ratio']:.1%}")
        
        # Show transliteration
        latin = transliterator.transliterate_to_latin(text)
        print(f"  Latin: {latin}")


def main():
    """Run all demonstrations."""
    try:
        demo_basic_transliteration()
        demo_file_processing()
        demo_coverage_analysis()
        
        print("\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()