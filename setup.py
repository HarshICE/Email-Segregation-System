#!/usr/bin/env python3
"""
Setup script for the Email Segregation System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="email-segregation-system",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An intelligent email processing system that automatically classifies and forwards emails",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/email-segregation-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pymongo>=4.6.0",
        "beautifulsoup4>=4.12.2",
        "cleantext>=1.1.4",
        "scikit-learn>=1.3.2",
        "monkeylearn>=3.6.0",
        "python-dotenv>=1.0.0",
        "lxml>=4.9.3",
        "pandas>=2.1.4",
        "numpy>=1.24.3",
        "email-validator>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "email-segregation=main:main",
        ],
    },
)
