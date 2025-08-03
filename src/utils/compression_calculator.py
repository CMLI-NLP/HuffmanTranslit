"""
Compression analysis utilities for transliteration methods.

This module provides functions to calculate file size and token compression
ratios when comparing original text with transliterated versions.
"""

import os
from typing import Dict, List, Optional, Tuple
from transformers import AutoTokenizer
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
import time


class CompressionAnalyzer:
    """Analyzer for calculating compression ratios of transliteration methods."""
    
    def __init__(self, tokenizer_path: str = "meta-llama/Llama-2-7b-hf"):
        """
        Initialize the compression analyzer.
        
        Args:
            tokenizer_path: Path or name of the tokenizer to use for token counting
        """
        self.tokenizer_path = tokenizer_path
        self.tokenizer = None
        self._load_tokenizer()
    
    def _load_tokenizer(self) -> None:
        """Load the tokenizer for token counting."""
        try:
            print("Loading tokenizer...")
            start_time = time.time()
            self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
            print(f"Tokenizer loaded in {time.time() - start_time:.2f} seconds")
        except Exception as e:
            print(f"Warning: Could not load tokenizer from {self.tokenizer_path}: {e}")
            print("Token compression analysis will be disabled.")
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(file_path)
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using the loaded tokenizer."""
        if self.tokenizer is None:
            raise ValueError("Tokenizer not available")
        return len(self.tokenizer(text).input_ids)
    
    def analyze_file_pair(self, original_file: str, transliterated_file: str, 
                         language: str) -> Dict[str, float]:
        """
        Analyze compression ratios between original and transliterated files.
        
        Args:
            original_file: Path to original text file
            transliterated_file: Path to transliterated text file
            language: Language identifier
            
        Returns:
            Dictionary containing compression analysis results
        """
        # Get file sizes
        original_size = self.get_file_size(original_file)
        transliterated_size = self.get_file_size(transliterated_file)
        
        # Calculate file size ratio
        file_size_ratio = original_size / transliterated_size if transliterated_size > 0 else float('inf')
        
        result = {
            'language': language,
            'original_file_size': original_size,
            'transliterated_file_size': transliterated_size,
            'file_size_ratio': file_size_ratio,
        }
        
        # Calculate token ratios if tokenizer is available
        if self.tokenizer is not None:
            try:
                # Read file contents
                with open(original_file, 'r', encoding='utf-8') as f:
                    original_text = f.read()
                with open(transliterated_file, 'r', encoding='utf-8') as f:
                    transliterated_text = f.read()
                
                # Count tokens
                original_tokens = self.count_tokens(original_text)
                transliterated_tokens = self.count_tokens(transliterated_text)
                
                token_ratio = original_tokens / transliterated_tokens if transliterated_tokens > 0 else float('inf')
                
                result.update({
                    'original_tokens': original_tokens,
                    'transliterated_tokens': transliterated_tokens,
                    'token_ratio': token_ratio,
                })
            except Exception as e:
                print(f"Warning: Could not analyze tokens for {language}: {e}")
        
        return result
    
    def analyze_multiple_files(self, file_pairs: List[Tuple[str, str, str]], 
                              max_workers: Optional[int] = None) -> List[Dict[str, float]]:
        """
        Analyze multiple file pairs in parallel.
        
        Args:
            file_pairs: List of (original_file, transliterated_file, language) tuples
            max_workers: Maximum number of worker threads
            
        Returns:
            List of compression analysis results
        """
        if max_workers is None:
            max_workers = min(len(file_pairs), mp.cpu_count())
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.analyze_file_pair, orig, trans, lang)
                for orig, trans, lang in file_pairs
            ]
            results = [future.result() for future in futures]
        
        return results
    
    def print_compression_summary(self, results: List[Dict[str, float]]) -> None:
        """
        Print a formatted summary of compression analysis results.
        
        Args:
            results: List of compression analysis results
        """
        print("\nCompression Analysis Results:")
        print("-" * 80)
        print(f"{'Language':^10} {'File Size Ratio':^15} {'Token Ratio':^15} {'File Size (KB)':^20}")
        print("-" * 80)
        
        for result in results:
            lang = result['language']
            file_ratio = result['file_size_ratio']
            token_ratio = result.get('token_ratio', 'N/A')
            file_size_kb = result['original_file_size'] / 1024
            
            token_ratio_str = f"{token_ratio:.2f}" if isinstance(token_ratio, float) else str(token_ratio)
            
            print(f"{lang:^10} {file_ratio:>8.2f}x {' '*5} {token_ratio_str:>8}x {' '*5} {file_size_kb:>8.1f}")
        
        print("-" * 80)
        
        # Calculate averages
        file_ratios = [r['file_size_ratio'] for r in results if r['file_size_ratio'] != float('inf')]
        token_ratios = [r['token_ratio'] for r in results 
                       if 'token_ratio' in r and r['token_ratio'] != float('inf')]
        
        if file_ratios:
            avg_file_ratio = sum(file_ratios) / len(file_ratios)
            print(f"Average file size compression: {avg_file_ratio:.2f}x")
        
        if token_ratios:
            avg_token_ratio = sum(token_ratios) / len(token_ratios)
            print(f"Average token compression: {avg_token_ratio:.2f}x")


def calculate_method_compression(base_dir: str, languages: List[str], 
                               method_name: str = "transliterated") -> Dict[str, Dict[str, float]]:
    """
    Calculate compression ratios for a specific transliteration method.
    
    Args:
        base_dir: Base directory containing the files
        languages: List of language codes
        method_name: Name of the transliteration method
        
    Returns:
        Dictionary mapping languages to their compression metrics
    """
    analyzer = CompressionAnalyzer()
    
    file_pairs = []
    for lang in languages:
        original_file = os.path.join(base_dir, f"{lang}_restored.txt")
        transliterated_file = os.path.join(base_dir, f"{lang}_latin.txt")
        
        if os.path.exists(original_file) and os.path.exists(transliterated_file):
            file_pairs.append((original_file, transliterated_file, lang))
        else:
            print(f"Warning: Missing files for language {lang}")
    
    if not file_pairs:
        print("No valid file pairs found")
        return {}
    
    results = analyzer.analyze_multiple_files(file_pairs)
    analyzer.print_compression_summary(results)
    
    # Convert to dictionary format
    compression_dict = {}
    for result in results:
        lang = result['language']
        compression_dict[lang] = {
            'file_size_ratio': result['file_size_ratio'],
            'token_ratio': result.get('token_ratio', None),
            'original_size_kb': result['original_file_size'] / 1024,
            'transliterated_size_kb': result['transliterated_file_size'] / 1024,
        }
    
    return compression_dict


def compare_methods(base_dirs: Dict[str, str], languages: List[str]) -> None:
    """
    Compare compression ratios across different transliteration methods.
    
    Args:
        base_dirs: Dictionary mapping method names to their base directories
        languages: List of language codes to analyze
    """
    print("Comparing transliteration methods...")
    
    all_results = {}
    for method_name, base_dir in base_dirs.items():
        print(f"\nAnalyzing method: {method_name}")
        all_results[method_name] = calculate_method_compression(base_dir, languages, method_name)
    
    # Print comparison table
    print("\n" + "="*100)
    print("METHOD COMPARISON SUMMARY")
    print("="*100)
    
    for lang in languages:
        print(f"\nLanguage: {lang.upper()}")
        print("-" * 60)
        print(f"{'Method':<20} {'File Ratio':<12} {'Token Ratio':<12} {'Size (KB)':<12}")
        print("-" * 60)
        
        for method_name, results in all_results.items():
            if lang in results:
                metrics = results[lang]
                file_ratio = metrics['file_size_ratio']
                token_ratio = metrics['token_ratio']
                size_kb = metrics['original_size_kb']
                
                token_str = f"{token_ratio:.2f}x" if token_ratio is not None else "N/A"
                print(f"{method_name:<20} {file_ratio:<8.2f}x {'':>3} {token_str:<12} {size_kb:<8.1f}")