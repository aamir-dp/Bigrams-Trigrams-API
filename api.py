from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from collections import Counter
from nltk.util import ngrams
from string import punctuation
import spacy

# Load the spaCy model
nlp = spacy.load("ru_core_news_sm")

# FastAPI app
app = FastAPI(title="NLP API", description="API for generating unigrams, bigrams, and trigrams.")

# Request model
class TextData(BaseModel):
    text: str
    ngram_size: int = 1  # Default to unigrams
    top_n: int = 10      # Default to top 10

# Preprocess text
def preprocess_text(text: str):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if token.is_alpha and token.text not in nlp.Defaults.stop_words and token.text not in punctuation
    ]
    return tokens

# Generate n-grams
def generate_ngrams(tokens: List[str], n: int):
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
