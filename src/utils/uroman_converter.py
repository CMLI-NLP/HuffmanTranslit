"""
UROMAN-based romanization utilities for comparison with Huffman transliteration.

This module provides wrapper functions for the UROMAN universal romanization
tool, allowing batch processing and comparison with our Huffman-based approach.
"""

import os
import traceback
from multiprocessing import Pool, cpu_count
from typing import List, Optional, Dict
import tqdm

try:
    import uroman as ur
    UROMAN_AVAILABLE = True
except ImportError:
    UROMAN_AVAILABLE = False
    print("Warning: uroman package not available. UROMAN conversion will be disabled.")


class UROMANConverter:
    """Wrapper for UROMAN universal romanization tool."""
    
    def __init__(self):
        """Initialize the UROMAN converter."""
        if not UROMAN_AVAILABLE:
            raise ImportError("uroman package is required but not available")
        
        self.uroman = ur.Uroman()
    
    def romanize_text(self, text: str, language_code: str) -> str:
        """
        Romanize a single text string using UROMAN.
        
        Args:
            text: Input text to romanize
            language_code: ISO language code (e.g., 'bod', 'mon', 'uig')
            
        Returns:
            Romanized text
        """
        if not text.strip():
            return text
            
        try:
            romanized = self.uroman.romanize_string(text, lcode=language_code)
            return romanized if romanized else text
        except Exception as e:
            print(f"Error romanizing text: {text[:50]}...")
            print(f"Error details: {str(e)}")
            return text
    
    def romanize_lines(self, lines: List[str], language_code: str) -> List[str]:
        """
        Romanize a list of text lines.
        
        Args:
            lines: List of text lines to romanize
            language_code: ISO language code
            
        Returns:
            List of romanized lines
        """
        results = []
        for line in lines:
            romanized = self.romanize_text(line.strip(), language_code)
            results.append(romanized)
        return results


def _process_chunk(args):
    """Process a chunk of lines with UROMAN (for multiprocessing)."""
    chunk, lang_code = args
    try:
        uroman = ur.Uroman()
        results = []
        
        for line in chunk:
            line = line.strip()
            if not line:
                results.append('')
                continue
                
            try:
                romanized = uroman.romanize_string(line, lcode=lang_code)
                results.append(romanized if romanized else line)
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Error details: {str(e)}")
                results.append(line)
                
        return results
    except Exception as e:
        print(f"Chunk processing error: {str(e)}")
        traceback.print_exc()
        return [line.strip() for line in chunk]


def convert_file_uroman(input_path: str, output_path: str, language_code: str, 
                       chunk_size: int = 100, num_processes: Optional[int] = None) -> bool:
    """
    Convert a text file using UROMAN romanization.
    
    Args:
        input_path: Path to input text file
        output_path: Path to output romanized file
        language_code: ISO language code for UROMAN
        chunk_size: Number of lines to process per chunk
        num_processes: Number of processes to use (None for auto)
        
    Returns:
        True if conversion successful, False otherwise
    """
    if not UROMAN_AVAILABLE:
        print("Error: UROMAN not available")
        return False
    
    try:
        print(f"Processing {os.path.basename(input_path)} with UROMAN (language: {language_code})...")
        
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Split into chunks for parallel processing
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
        process_args = [(chunk, language_code) for chunk in chunks]
        
        # Set number of processes
        if num_processes is None:
            num_processes = cpu_count()
        
        # Process chunks in parallel
        with Pool(processes=num_processes) as pool:
            results = []
            for result in tqdm.tqdm(
                pool.imap(_process_chunk, process_args),
                total=len(chunks),
                desc=f"Converting {os.path.basename(input_path)}"
            ):
                results.extend(result)
        
        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Write output file
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in results:
                f.write(line + '\n')
        
        print(f"Successfully converted {os.path.basename(input_path)} to {os.path.basename(output_path)}")
        return True
        
    except Exception as e:
        print(f"Error processing file {input_path}:")
        print(f"Error details: {str(e)}")
        traceback.print_exc()
        return False


def batch_convert_uroman(file_configs: List[Dict[str, str]], 
                        chunk_size: int = 100) -> List[bool]:
    """
    Convert multiple files using UROMAN in batch.
    
    Args:
        file_configs: List of dictionaries with 'input', 'output', 'lang_code' keys
        chunk_size: Number of lines to process per chunk
        
    Returns:
        List of boolean success indicators
    """
    if not UROMAN_AVAILABLE:
        print("Error: UROMAN not available")
        return [False] * len(file_configs)
    
    results = []
    for config in file_configs:
        success = convert_file_uroman(
            input_path=config['input'],
            output_path=config['output'],
            language_code=config['lang_code'],
            chunk_size=chunk_size
        )
        results.append(success)
    
    return results


def get_language_code_mapping() -> Dict[str, str]:
    """
    Get mapping from our language codes to UROMAN language codes.
    
    Returns:
        Dictionary mapping language codes
    """
    return {
        'bo': 'bod',    # Tibetan
        'mn': 'mon',    # Mongolian
        'ug': 'uig',    # Uyghur
        'zh': 'zho'     # Chinese
    }


def setup_uroman_comparison(base_input_dir: str, base_output_dir: str, 
                           languages: List[str]) -> List[Dict[str, str]]:
    """
    Set up file configurations for UROMAN comparison.
    
    Args:
        base_input_dir: Base directory containing input files
        base_output_dir: Base directory for output files
        languages: List of language codes
        
    Returns:
        List of file configuration dictionaries
    """
    lang_mapping = get_language_code_mapping()
    file_configs = []
    
    for lang in languages:
        if lang not in lang_mapping:
            print(f"Warning: No UROMAN language code for {lang}")
            continue
            
        input_file = os.path.join(base_input_dir, f"{lang}_restored.txt")
        output_file = os.path.join(base_output_dir, f"{lang}_uroman.txt")
        
        if not os.path.exists(input_file):
            print(f"Warning: Input file not found: {input_file}")
            continue
            
        config = {
            'input': input_file,
            'output': output_file,
            'lang_code': lang_mapping[lang]
        }
        file_configs.append(config)
    
    return file_configs


def compare_with_huffman(huffman_dir: str, uroman_dir: str, languages: List[str]) -> None:
    """
    Compare Huffman transliteration results with UROMAN romanization.
    
    Args:
        huffman_dir: Directory containing Huffman transliteration results
        uroman_dir: Directory containing UROMAN romanization results
        languages: List of language codes to compare
    """
    print("\nComparing Huffman Transliteration vs UROMAN Romanization")
    print("=" * 60)
    
    for lang in languages:
        huffman_file = os.path.join(huffman_dir, f"{lang}_latin.txt")
        uroman_file = os.path.join(uroman_dir, f"{lang}_uroman.txt")
        
        if not os.path.exists(huffman_file) or not os.path.exists(uroman_file):
            print(f"Skipping {lang}: Missing files")
            continue
        
        # Compare file sizes
        huffman_size = os.path.getsize(huffman_file) / 1024  # KB
        uroman_size = os.path.getsize(uroman_file) / 1024    # KB
        
        print(f"\nLanguage: {lang.upper()}")
        print(f"Huffman file size: {huffman_size:.1f} KB")
        print(f"UROMAN file size:  {uroman_size:.1f} KB")
        print(f"Size ratio (Huffman/UROMAN): {huffman_size/uroman_size:.2f}")
        
        # Sample comparison
        try:
            with open(huffman_file, 'r', encoding='utf-8') as f:
                huffman_sample = f.readline().strip()
            with open(uroman_file, 'r', encoding='utf-8') as f:
                uroman_sample = f.readline().strip()
            
            print(f"Sample Huffman: {huffman_sample[:100]}...")
            print(f"Sample UROMAN:  {uroman_sample[:100]}...")
            
        except Exception as e:
            print(f"Error reading sample: {e}")