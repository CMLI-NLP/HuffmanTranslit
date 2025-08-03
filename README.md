# HuffmanTranslit: Reversible Transliteration for Low-Resource Languages

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper](https://img.shields.io/badge/Paper-ACL2025-green.svg)](https://aclanthology.org/2025.acl-long.795/)

**HuffmanTranslit** is a novel framework for enhancing cross-lingual transfer in large language models through reversible transliteration of low-resource languages. Our approach combines character transliteration with Huffman coding principles to achieve compression, accuracy, efficiency, and scalability.

## 🎯 Key Features

- **100% Lossless Conversion**: Guaranteed reversible transliteration between original scripts and Latin representations
- **High Compression**: Up to 50% reduction in file size and 50-80% reduction in token count
- **Multi-Strategy Support**: Three progressive transliteration strategies (Basic, Tokenizer-optimized, Hybrid)
- **Multi-Language**: Support for Tibetan, Mongolian, and Uyghur languages
- **Easy Integration**: Simple API for seamless integration into existing NLP pipelines

## 📖 Citation

If you use this work in your research, please cite our ACL 2025 paper:

```bibtex
@inproceedings{zhuang2025enhancing,
  title={Enhancing Cross-Lingual Transfer through Reversible Transliteration: A Huffman-Based Approach for Low-Resource Languages},
  author={Zhuang, Wenhao and Sun, Yuan and Zhao, Xiaobing},
  booktitle={Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={16299--16313},
  year={2025}
}
```

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/CMLI-NLP/HuffmanTranslit.git
cd HuffmanTranslit
pip install -r requirements.txt
```

### Basic Usage

```python
from src.core.transliterator import create_transliterator

# Create a transliterator with optimized encoding
transliterator = create_transliterator('optimized')

# Transliterate text to Latin representation
tibetan_text = "འཇིག་རྟེན་གྱི་སངས་རྒྱས་ཆོས་ལུགས།"
latin_text = transliterator.transliterate_to_latin(tibetan_text)
print(f"Latin: {latin_text}")

# Restore original text (100% lossless)
restored_text = transliterator.transliterate_from_latin(latin_text)
print(f"Restored: {restored_text}")
print(f"Lossless: {tibetan_text == restored_text}")  # True
```

### Run Examples

```bash
# Basic transliteration demo
python examples/basic_demo.py

# Compression analysis demo  
python examples/compression_demo.py
```

## 🏗️ Framework Architecture

### Three-Stage Processing Pipeline

1. **Character Encoding Design**: Analyze character frequencies and design custom encodings
2. **Transliteration and Model Training**: Convert text using frequency-based character mappings  
3. **End-to-End Language Processing**: Automated language detection and processing pipeline

### Encoding Strategies

| Strategy | Description | Vocabulary Size | Compression Ratio |
|----------|-------------|-----------------|-------------------|
| **Basic** | Simple frequency-based Latin encoding | 32,000 | 1.63× |
| **Tokenizer** | LLaMA2 single-token optimization | 32,000 | 2.35× |
| **Hybrid** | Specialized vocabulary integration | 33,738 | 3.04× |

## 📊 Performance Results

### Cross-Lingual Transfer Performance

| Task | Tibetan | Mongolian | Uyghur | Average |
|------|---------|-----------|--------|---------|
| **Text Classification** | 54.14% | 61.25% | 81.00% | 65.46% |
| **Reading Comprehension** | 16.0 EM | - | - | - |
| **Machine Translation** | 6.3 BLEU | - | 7.0 BLEU | - |

### Compression Efficiency

- **File Size**: 2-3× compression ratio
- **Token Count**: 2-5× compression ratio  
- **Storage Savings**: Up to 50% reduction

## 🗂️ Project Structure

```
HuffmanTranslit/
├── src/
│   ├── core/
│   │   └── transliterator.py      # Main transliteration engine
│   ├── utils/
│   │   ├── char_analyzer.py       # Character frequency analysis
│   │   ├── compression_calculator.py  # Compression ratio calculation
│   │   └── uroman_converter.py    # UROMAN comparison utilities
│   └── evaluation/
├── data/
│   ├── character_mappings/        # Pre-built character mappings
│   └── samples/                   # Sample data files
├── examples/                      # Usage examples and demos
└── tests/                        # Unit tests
```

## 🔧 Advanced Usage

### Character Analysis and Mapping Generation

```python
from src.utils.char_analyzer import CharacterAnalyzer

# Analyze character frequencies in your corpus
analyzer = CharacterAnalyzer()
analyzer.analyze_file('your_corpus.txt')

# Generate optimized character mappings
mappings = analyzer.create_basic_mapping()
analyzer.save_mapping_json(mappings, 'custom_mapping.json')
```

### Compression Analysis

```python
from src.utils.compression_calculator import CompressionAnalyzer

# Analyze compression ratios
analyzer = CompressionAnalyzer()
result = analyzer.analyze_file_pair(
    'original.txt', 
    'transliterated.txt', 
    'tibetan'
)
print(f"Compression ratio: {result['file_size_ratio']:.2f}x")
```

### Comparison with UROMAN

```python
from src.utils.uroman_converter import convert_file_uroman

# Convert using UROMAN for comparison
convert_file_uroman(
    'input.txt', 
    'output_uroman.txt', 
    'bod'  # Tibetan language code
)
```

## 📚 Datasets

### Training Data
- **CUTE Multilingual Dataset**: [https://huggingface.co/datasets/CMLI-NLP/CUTE-Datasets](https://huggingface.co/datasets/CMLI-NLP/CUTE-Datasets)
- **Mongolian Pretraining Dataset**: [https://huggingface.co/datasets/CMLI-NLP/Mongolian-pretrain-dataset](https://huggingface.co/datasets/CMLI-NLP/Mongolian-pretrain-dataset)

### Character Mappings
- **Basic Mapping**: Frequency-based Latin character assignments
- **Optimized Mapping**: LLaMA2 tokenizer-optimized single-token encodings

## 🌍 Supported Languages

| Language | ISO Code | Script | Status |
|----------|----------|--------|--------|
| Tibetan | bo | Tibetan script | ✅ Full support |
| Mongolian | mn | Traditional Mongolian | ✅ Full support |
| Uyghur | ug | Uyghur Arabic script | ✅ Full support |

## 🔬 Technical Details

### Huffman Coding Properties
- **Variable-length allocation**: High-frequency characters get shorter codes
- **Prefix property**: No code is a prefix of another (ensures unambiguous decoding)
- **Compression efficiency**: Optimal character-level compression

### Encoding Pattern Design
```
Length 1: A, B, ..., Z (26 codes)
Length 2: Aa, Ab, ..., Zz (676 codes) 
Length 3: Aaa, Aab, ..., Zzz (17,576 codes)
Total capacity: 475,254 characters
```

## ⚡ Requirements

- Python 3.8+
- transformers >= 4.20.0
- uroman (optional, for comparison)
- tqdm
- pathlib

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details on:
- Code style and standards
- Testing requirements  
- Pull request process
- Issue reporting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This work is supported by:
- National Social Science Foundation (22&ZD035)
- National Nature Science Foundation (61972436)  
- Minzu University of China Foundation (GRSCP202316, 2023QNYL22, 2024GJYY43)

## 📞 Contact

- **Wenhao Zhuang**: sdrz_zwh@163.com
- **Yuan Sun**: sunyuan@muc.edu.cn (Corresponding author)
- **Xiaobing Zhao**: nmzxb_cn@163.com

## 🔗 Related Resources

- [Paper (ACL 2025)](https://aclanthology.org/2025.acl-long.795/)
- [CUTE Dataset](https://huggingface.co/datasets/CMLI-NLP/CUTE-Datasets)
- [Mongolian Dataset](https://huggingface.co/datasets/CMLI-NLP/Mongolian-pretrain-dataset)
- [Minzu University NLP Lab](https://github.com/CMLI-NLP)

---

*For detailed technical information, please refer to our ACL 2025 paper and the documentation in the `docs/` directory.*