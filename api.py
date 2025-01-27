from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from fastapi.middleware.cors import CORSMiddleware
import logging
import re
import nltk

# Ensure necessary NLTK resources are available
nltk.download("punkt")
nltk.download("stopwords")

# Initialize FastAPI app
app = FastAPI(title="Keyword Extraction API", description="API for generating unigrams, bigrams, trigrams, etc.")

# Preload English stopwords
stop_words = set(stopwords.words('english'))

# Function to extract n-grams
def extract_keywords_with_counts(text: str, ngram_range: int = 1) -> List[dict]:
    # Normalize the text: Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)  # Keep only alphanumeric and whitespace
    words = word_tokenize(text.lower())  # Tokenize and convert to lowercase

    # Ensure all tokens are strings and remove non-alphabetic tokens
    filtered_words = [word for word in words if isinstance(word, str) and word.isalpha() and word not in stop_words]

    # Check if there are enough words for the requested n-gram size
    if len(filtered_words) < ngram_range:
        return []  # Return empty if insufficient words

    # Generate n-grams
    if ngram_range > 1:
        ngram_words = [' '.join(ng) for ng in ngrams(filtered_words, ngram_range)]
        keywords = Counter(ngram_words).most_common(20)  # Top 20 n-grams
    else:
        keywords = Counter(filtered_words).most_common(20)  # Top 20 unigrams

    return [{"keyword": keyword, "count": count} for keyword, count in keywords]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this to specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

logging.basicConfig(level=logging.DEBUG) #vercel debug logging

# Request model
class TextData(BaseModel):
    text: str
    ngram_size: int = 1  # Default to unigrams

# Define the `/ngrams` endpoint
@app.post("/ngrams")
def get_keywords(data: TextData):
    try:
        print(f"Input Text: {data.text}")
        print(f"N-Gram Size: {data.ngram_size}")

        # Extract keywords
        keywords = extract_keywords_with_counts(data.text, ngram_range=data.ngram_size)
        print(f"Extracted Keywords: {keywords}")

        return {
            "ngram_size": data.ngram_size,
            "keywords": keywords
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
