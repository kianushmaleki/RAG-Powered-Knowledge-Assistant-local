import numpy as np
import os
import time
from utils.decorators import timer_decorator

def normalize(vectors: np.ndarray) -> np.ndarray:
    '''
    Normalizes the input vectors to have unit length.
    Args:
        vectors (np.ndarray): A 2D array of shape (n_samples, n_features) containing the vectors to be normalized.
    Returns:
        np.ndarray: The normalized vectors.
    '''
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

# read the txt files from the data folder
documents = []
@timer_decorator
def load_documents(data_folder) -> None:
    '''
    Loads all .txt files from the specified folder and appends their content to the 'documents' list.
    Args:
        data_folder (str): The path to the folder containing .txt files.
    '''
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(data_folder, filename), "r", encoding="utf-8") as file:
                documents.append(file.read())
