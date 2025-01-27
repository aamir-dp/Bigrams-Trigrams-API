#!/usr/bin/env bash

# Pre-download NLTK stopwords resource
python -c "import nltk; nltk.download('stopwords', download_dir='/tmp/nltk_data')"

# Start the FastAPI application
uvicorn api:app --host 0.0.0.0 --port $PORT
