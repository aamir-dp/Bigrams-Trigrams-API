import nltk
import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import re

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aamir-dp.github.io"],  # Replace with your frontend domain
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type", "api_key"],
)

# Set NLTK data directory to a writable location (e.g., /tmp)
nltk_path = "/tmp/nltk_data"
os.makedirs(nltk_path, exist_ok=True)
nltk.data.path.append(nltk_path)

# Ensure necessary NLTK resources are available
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", download_dir=nltk_path)  # Download stopwords dynamically
    stop_words = set(stopwords.words("english"))

# Function to extract n-grams
def extract_keywords_with_counts(text: str, ngram_range: int = 1):
    text = re.sub(r"[^\w\s]", "", text)
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

    if len(filtered_words) < ngram_range:
        return []

    if ngram_range > 1:
        ngram_words = [" ".join(ng) for ng in ngrams(filtered_words, ngram_range)]
        keywords = Counter(ngram_words).most_common(20)
    else:
        keywords = Counter(filtered_words).most_common(20)

    return [{"keyword": keyword, "count": count} for keyword, count in keywords]

# API endpoint
class TextData(BaseModel):
    text: str
    ngram_size: int = 1

@app.post("/ngrams")
def get_keywords(data: TextData, api_key: str = Header(None)):
    if api_key != os.getenv("API_KEY"):  # Validate API key
        raise HTTPException(status_code=401, detail="Unauthorized")

    keywords = extract_keywords_with_counts(data.text, data.ngram_size)
    return {"ngram_size": data.ngram_size, "keywords": keywords}
