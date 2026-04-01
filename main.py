'''
Project description >>>
Customer Support Assistant: 
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os 
import atexit
import torch
from typing import List
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

from utils import *
from utils import print_timing_summary

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import re
from typing import List, Dict
from sentence_transformers import util
import chromadb
from chromadb.utils import embedding_functions

from utils.functions import normalize
from utils.decorators import timer_decorator



print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print("\n✨ All imports successful!")



question = "What is name of the company?" 
my_chunk_size = 300
my_overlap = 100

download_documents = input("Do you want to download the documents? (y/n): ")
if download_documents.lower() == 'y':
    # Simulate downloading documents (you can replace this with actual download code)
    print("Downloading documents...")
    
    print("Documents downloaded successfully!")
else:
    print("Skipping document download.")






@timer_decorator
def chunk_text(text: str, tokenizer, chunk_size: int = my_chunk_size, overlap: int = my_overlap ) -> List[str]:
    '''
    Splits the input text into chunks of specified size with a certain overlap, ensuring that tokenization is respected.
    Args:
        text (str): The input text to be chunked.
        tokenizer: The tokenizer used to convert text into tokens.
        chunk_size (int): The maximum number of tokens in each chunk.
        overlap (int): The number of tokens that overlap between consecutive chunks.
    Returns:
        List[str]: A list of text chunks.
    '''
    # Add truncation=False to suppress the warning since we are manually chunking
    inputs = tokenizer(text, add_special_tokens=False, return_tensors="pt", truncation=False)
    input_ids = inputs["input_ids"][0]

    chunks = []
    for i in range(0, len(input_ids), chunk_size - overlap):
        chunk_ids = input_ids[i : i + chunk_size]
        chunks.append(tokenizer.decode(chunk_ids, skip_special_tokens=True))
    return chunks



# Load the model and tokenizer directly
model_name = "distilbert-base-cased-distilled-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name,truncation=False)
qa_model = AutoModelForQuestionAnswering.from_pretrained(model_name)

my_data_folder = 'data'
load_documents(my_data_folder)
documents = load_documents(my_data_folder)
print(f"Loaded {len(documents)} documents from '{my_data_folder}' folder.")
context = "\n\n".join(documents)
context_chunks = chunk_text(context, tokenizer)

best_answer = ''
best_score = float('-inf')
for i, chunk in enumerate(context_chunks):
    inputs = tokenizer(question, chunk, return_tensors="pt",truncation=True, max_length=512)
    with torch.no_grad():
        outputs = qa_model(**inputs)
    

    # Get the max raw scores
    start_logit_score, answer_start = torch.max(outputs.start_logits, dim=-1)
    end_logit_score, answer_end = torch.max(outputs.end_logits, dim=-1)
    total_raw_score = start_logit_score.item() + end_logit_score.item() # .item() is crucial here to get the number out of the PyTorch wrapper

    # Get Answer String
    current_answer = tokenizer.decode(inputs.input_ids[0][answer_start : answer_end + 1])
    
    # CLEANING: If the model picks the [CLS] token or the question itself, ignore it
    current_answer = current_answer.replace("[CLS]", "").strip()
    current_answer = tokenizer.decode(inputs.input_ids[0][answer_start : answer_end + 1], skip_special_tokens=True).strip()

    # 3. Update Best Answer
    # We only update if the score is better AND the answer isn't empty/junk
    if total_raw_score > best_score and len(current_answer) > 0:
        best_score = total_raw_score
        best_answer = current_answer


atexit.register(print_timing_summary)
print(f"\n✅ Final Best Answer: {best_answer}")
print(f"📈 Confidence Score (Raw): {best_score:.4f}")