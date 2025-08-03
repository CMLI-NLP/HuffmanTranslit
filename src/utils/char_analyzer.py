"""
Character frequency analysis and encoding assignment utilities.

This module provides tools for analyzing character frequencies in text corpora
and generating optimal character encodings based on frequency distributions.
"""

import json
import unicodedata
from collections import Counter
from typing import Dict, List, Tuple, Optional
import os


class CharacterAnalyzer:
    """Analyzer for character frequency and encoding assignment."""
    
    def __init__(self):
        """Initialize the character analyzer."""
        self.char_frequencies: Dict[str, int] = {}
        self.total_chars = 0
    
    def analyze_text(self, text: str) -> None:
        """
        Analyze character frequencies in given text.
        
        Args:
            text: Input text to analyze
        """
        counter = Counter(text)
        for char, freq in counter.items():
            self.char_frequencies[char] = self.char_frequencies.get(char, 0) + freq
            self.total_chars += freq
    
    def analyze_file(self, file_path: str, encoding: str = 'utf-8') -> None:
        """
        Analyze character frequencies in a text file.
        
        Args:
            file_path: Path to the text file
            encoding: File encoding (default: utf-8)
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                for line in f:
                    self.analyze_text(line)
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
    
    def analyze_multiple_files(self, file_paths: List[str], encoding: str = 'utf-8') -> None:
        """
        Analyze character frequencies across multiple files.
        
        Args:
            file_paths: List of file paths to analyze
            encoding: File encoding (default: utf-8)
        """
        for file_path in file_paths:
            if os.path.exists(file_path):
                print(f"Analyzing {file_path}...")
                self.analyze_file(file_path, encoding)
            else:
                print(f"Warning: File not found: {file_path}")
    
    def get_sorted_characters(self, min_frequency: int = 1) -> List[Tuple[str, int]]:
        """
        Get characters sorted by frequency (descending).
        
        Args:
            min_frequency: Minimum frequency threshold
            
        Returns:
            List of (character, frequency) tuples sorted by frequency
        """
        filtered_chars = {char: freq for char, freq in self.char_frequencies.items() 
                         if freq >= min_frequency}
        return sorted(filtered_chars.items(), key=lambda x: x[1], reverse=True)
    
    def export_analysis(self, output_file: str, min_frequency: int = 1) -> None:
        """
        Export character analysis to a TSV file.
        
        Args:
            output_file: Output file path
            min_frequency: Minimum frequency threshold
        """
        sorted_chars = self.get_sorted_characters(min_frequency)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("字符\tUnicode\t名称\t频率\n")
            for char, freq in sorted_chars:
                unicode_point = f"U+{ord(char):04X}"
                try:
                    char_name = unicodedata.name(char)
                except ValueError:
                    char_name = "UNKNOWN"
                f.write(f"{char}\t{unicode_point}\t{char_name}\t{freq}\n")
        
        print(f"Character analysis exported to {output_file}")
    
    def create_basic_mapping(self, num_chars: Optional[int] = None) -> List[Dict]:
        """
        Create basic character mapping with simple Latin codes.
        
        Args:
            num_chars: Number of top characters to include (None for all)
            
        Returns:
            List of character mapping dictionaries
        """
        sorted_chars = self.get_sorted_characters()
        if num_chars:
            sorted_chars = sorted_chars[:num_chars]
        
        mappings = []
        code_id = 1
        
        # Generate encoding patterns: B-Z, then Aa-Az, Ba-Bz, etc.
        single_codes = [chr(ord('B') + i) for i in range(25)]  # B-Z (excluding A)
        double_codes = []
        for first in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            for second in 'abcdefghijklmnopqrstuvwxyz':
                double_codes.append(first + second)
        
        all_codes = single_codes + double_codes
        
        for i, (char, freq) in enumerate(sorted_chars):
            if i >= len(all_codes):
                print(f"Warning: Not enough codes for all characters. Stopping at {i} characters.")
                break
                
            unicode_point = f"U+{ord(char):04X}"
            try:
                char_name = unicodedata.name(char)
            except ValueError:
                char_name = "UNKNOWN"
            
            mapping = {
                "id": code_id,
                "char": char,
                "unicode": unicode_point,
                "name": char_name,
                "frequency": freq,
                "latin_code": all_codes[i]
            }
            mappings.append(mapping)
            code_id += 1
        
        return mappings
    
    def save_mapping_json(self, mappings: List[Dict], output_file: str) -> None:
        """
        Save character mappings to JSON file.
        
        Args:
            mappings: List of mapping dictionaries
            output_file: Output JSON file path
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, ensure_ascii=False, indent=2)
        
        print(f"Character mappings saved to {output_file}")
    
    def print_summary(self) -> None:
        """Print a summary of the character analysis."""
        print(f"\nCharacter Analysis Summary:")
        print(f"Total characters analyzed: {self.total_chars:,}")
        print(f"Unique characters found: {len(self.char_frequencies):,}")
        
        # Show top 10 characters
        sorted_chars = self.get_sorted_characters()
        print(f"\nTop 10 most frequent characters:")
        for i, (char, freq) in enumerate(sorted_chars[:10]):
            unicode_point = f"U+{ord(char):04X}"
            percentage = (freq / self.total_chars) * 100
            print(f"{i+1:2d}. '{char}' ({unicode_point}): {freq:,} ({percentage:.2f}%)")


def analyze_corpus_files(file_paths: List[str], output_dir: str, 
                        language_code: str) -> str:
    """
    Analyze a corpus and generate character mappings.
    
    Args:
        file_paths: List of corpus file paths
        output_dir: Output directory for results
        language_code: Language code (e.g., 'bo', 'mn', 'ug')
        
    Returns:
        Path to the generated mapping JSON file
    """
    analyzer = CharacterAnalyzer()
    
    # Analyze files
    analyzer.analyze_multiple_files(file_paths)
    analyzer.print_summary()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Export analysis
    analysis_file = os.path.join(output_dir, f"{language_code}_char_analysis.txt")
    analyzer.export_analysis(analysis_file)
    
    # Create and save mapping
    mappings = analyzer.create_basic_mapping()
    mapping_file = os.path.join(output_dir, f"{language_code}_mapping.json")
    analyzer.save_mapping_json(mappings, mapping_file)
    
    return mapping_file


def get_encoding_capacity(max_length: int = 4) -> Dict[int, int]:
    """
    Calculate theoretical encoding capacity for different code lengths.
    
    Args:
        max_length: Maximum code length to calculate
        
    Returns:
        Dictionary mapping code length to capacity
    """
    capacities = {}
    
    for length in range(1, max_length + 1):
        if length == 1:
            # Single uppercase letters (A-Z)
            capacity = 26
        else:
            # First letter uppercase, rest lowercase
            # 26 choices for first letter, 26^(length-1) for rest
            capacity = 26 * (26 ** (length - 1))
        
        capacities[length] = capacity
    
    # Calculate cumulative capacity
    total_capacity = sum(capacities.values())
    capacities['total'] = total_capacity
    
    return capacities


def print_encoding_capacity_table(max_length: int = 4) -> None:
    """
    Print a table showing encoding capacity at different lengths.
    
    Args:
        max_length: Maximum code length to show
    """
    capacities = get_encoding_capacity(max_length)
    
    print("\nEncoding Capacity Analysis:")
    print("-" * 40)
    print(f"{'Length':<8} {'Pattern':<15} {'Capacity':<12}")
    print("-" * 40)
    
    patterns = {
        1: "A, B, ..., Z",
        2: "Aa, Ab, ..., Zz", 
        3: "Aaa, Aab, ..., Zzz",
        4: "Aaaa, Aaab, ..., Zzzz"
    }
    
    for length in range(1, max_length + 1):
        pattern = patterns.get(length, f"{'A' + 'a' * (length-1)} pattern")
        capacity = capacities[length]
        print(f"{length:<8} {pattern:<15} {capacity:,}")
    
    print("-" * 40)
    print(f"{'Total':<8} {'(up to ' + str(max_length) + ' chars)':<15} {capacities['total']:,}")
    print("-" * 40)