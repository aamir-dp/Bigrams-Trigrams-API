from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import os
import re

# Load API key from environment variables
API_KEY = os.getenv("API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to restrict frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aamir-dp.github.io"],  # Replace with your frontend's domain
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type", "api_key"],
)

# Preload NLTK resources
nltk_path = os.path.join(os.path.dirname(__file__), "nltk_data")
stop_words = set(stopwords.words("english"))

# Function to generate n-grams
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

# Request model
class TextData(BaseModel):
    text: str
    ngram_size: int = 1

# API endpoint
@app.post("/ngrams")
def get_keywords(data: TextData, api_key: str = Header(None)):
    if api_key != API_KEY:  # Validate the API key
        raise HTTPException(status_code=401, detail="Unauthorized")

    keywords = extract_keywords_with_counts(data.text, ngram_range=data.ngram_size)
    return {"ngram_size": data.ngram_size, "keywords": keywords}
