# Vishing Defender
A comprehensive voice phishing detection system built using advanced data structures and algorithms.

## Overview
Vishing Defender is a comprehensive voice phishing detection system developed to combat the escalating threat of telephone scams. Built as an academic project demonstrating advanced data structures and algorithms, this application provides real-time protection against vishing attacks through multiple analysis methods.

## Features
- **Phone Number Analysis**: Binary search on sorted country codes, hash map lookup for reported numbers
- **Text Analysis**: Aho-Corasick algorithm + SVM machine learning for pattern detection
- **Audio Analysis**: Speech-to-text using Wav2Vec2 with sliding window processing
- **URL Analysis**: Aho-Corasick algorithm with Trie data structure for multi-pattern matching
- **Interactive Questionnaire**: Binary tree navigation with weighted risk scoring for different scam scenarios
- **Education Module**: Red-black tree implementation for quiz management
- **Real-time Risk Assessment**: Aggregated scoring system across all detection methods

## Project Structure
```
Vishing-Scam-Detection/
├── main.py                 # Main application entry point
├── checkphoneNumber.py     # Phone number and country code analysis
├── linkanalysis.py         # URL analysis using Aho-Corasick
├── SVMAho.py               # Text analysis with ML and pattern matching
├── analyzeWav.py           # Audio transcription and analysis
├── questionnaire.py        # Interactive risk assessment
├── education.py            # Educational content and quiz
├── riskValue.py            # Risk management system
├── home.py                 # Home page interface
├── Datasets/               # Training data and pattern databases
├── Speech to Text Test/    # Audio samples for testing
└── testDatasets/           # Datasets for testing
```

## Technical Implementation
### Data Structures
- **Trie**: URL pattern storage and retrieval
- **Hash Map**: Phone number frequency tracking
- **Binary Tree**: Questionnaire navigation
- **Left-Leaning Red-Black Tree**: Education quiz system
- **Arrays**: Country code storage with binary search

### Algorithms
- **Aho-Corasick**: Multi-pattern string matching for URL and text analysis
- **Merge Sort**: O(n log n) sorting for country codes
- **Binary Search**: O(log n) country code lookup
- **Depth-First Traversal**: Question tree navigation
- **TF-IDF Vectorization**: Text feature extraction
- **SVM Classification**: Machine learning-based text analysis

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/glenngx/Vishing-Scam-Detection.git
   ```
2. Install required packages:
   ```
   pip install streamlit pandas scikit-learn transformers torch torchaudio soundfile pyctcdecode numpy
   ```
3. Run the application:
   ```
   streamlit run main.py
   ```
   
