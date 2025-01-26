from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from collections import Counter
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation

# Download NLTK resources (if not already downloaded)
import nltk
nltk.data.path.append("C:/nltk_data")  # Update this path to where you saved the data

# FastAPI app
app = FastAPI(title="NLP API", description="API for generating unigrams, bigrams, and trigrams.")

# Request model
class TextData(BaseModel):
    text: str
    ngram_size: int = 1  # Default to unigrams
    top_n: int = 10      # Default to top 10

# Preprocess text
def preprocess_text(text: str) -> List[str]:
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())  # Tokenize and lowercase the text
    filtered_tokens = [
        token for token in tokens 
        if token.is_alpha and token not in stop_words and token not in punctuation
    ]
    return filtered_tokens

# Generate n-grams
def generate_ngrams(tokens: List[str], n: int) -> List[str]:
    return [' '.join(gram) for gram in ngrams(tokens, n)]

@app.post("/ngrams")
def get_ngrams(data: TextData):
    if data.ngram_size < 1:
        raise HTTPException(status_code=400, detail="N-gram size must be 1 or greater.")
    
    # Preprocess the input text
    tokens = preprocess_text(data.text)

    # Generate n-grams
    ngrams_list = generate_ngrams(tokens, data.ngram_size)
    
    # Count n-grams
    ngram_counts = Counter(ngrams_list)

    # Return the top N n-grams
    top_ngrams = ngram_counts.most_common(data.top_n)

    return {
        "ngram_size": data.ngram_size,
        "top_ngrams": [{"phrase": phrase, "count": count} for phrase, count in top_ngrams]
    }
