"""
Setup configuration for HuffmanTranslit package.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="huffmantranslit",
    version="1.0.0",
    author="Wenhao Zhuang, Yuan Sun, Xiaobing Zhao",
    author_email="sunyuan@muc.edu.cn",
    description="Reversible Transliteration for Low-Resource Languages using Huffman Coding",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/CMLI-NLP/HuffmanTranslit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "": ["../data/character_mappings/*.json"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
        "uroman": [
            "uroman>=1.2.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "huffman-translit=core.transliterator:main",
        ],
    },
    keywords="transliteration, low-resource languages, huffman coding, nlp, cross-lingual",
    project_urls={
        "Bug Reports": "https://github.com/CMLI-NLP/HuffmanTranslit/issues",
        "Source": "https://github.com/CMLI-NLP/HuffmanTranslit",
        "Documentation": "https://github.com/CMLI-NLP/HuffmanTranslit#readme",
        "Paper": "https://aclanthology.org/2025.acl-long.795/",
    },
)