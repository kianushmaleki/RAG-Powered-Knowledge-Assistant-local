# RAG-Powered Knowledge Assistant

- Context-Aware Text Chunking: Employs a sliding window approach with configurable chunk_size and overlap to ensure the NLP model processes large documents without losing information at the boundaries.

- High-Performance QA Extraction: Leverages AutoModelForQuestionAnswering and PyTorch to perform real-time inference, selecting answers based on the highest confidence logit scores across multiple document segments.

## Features
- Loads and processes multiple text documents from the `data/` folder
- Splits large documents into overlapping chunks for better context handling
- Uses transformer-based QA models (DistilBERT by default)
- Answers user questions by searching across all loaded documents
- Designed for easy model upgrades (swap in larger models for improved answers)

## Current Limitations
- Short or incomplete answers for complex, multi-sentence questions
- Best suited for simple factoid queries (e.g., company name)
- Next step: integrate a larger QA model for improved long-form answers

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd RAG-Powered Knowledge Assistant
   ```
2. (Recommended) Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Usage
1. Place your `.txt` documents in the `data/` folder.
2. Run the assistant:
   ```sh
   python main.py
   ```
3. Edit the `question` variable in `main.py` to change the query.

## Project Structure
```
.
├── main.py
├── data/
│   └── *.txt
├── utils/
│   ├── decorators.py
│   └── vector_ops.py
└── README.md
```

## Customization
- To use a larger QA model, change the `model_name` in `main.py` (e.g., try `bert-large-uncased-whole-word-masking-finetuned-squad`)
- Adjust chunk size and overlap for your documents as needed
