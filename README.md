
# **NLP API Documentation**

## **Overview**

This API processes a given text to generate **unigrams**, **bigrams**, or **trigrams**, and returns the most frequently occurring n-grams with their counts. It uses **FastAPI** for a fast, modern, and interactive API experience.

---

## **Installation**

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn spacy nltk
   python -m spacy download ru_core_news_sm
   ```

2. **Create the API Code**:
   Save the following code as `api.py`:

 
## **Running the API**

1. **Start the Server**:
   Run the following command in the terminal:
   ```bash
   uvicorn api:app --reload
   ```

2. **Access the Documentation**:
   Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view and interact with the API using the built-in Swagger UI.

---

## **Endpoints**

### **POST /ngrams**

#### **Description**
Generates unigrams, bigrams, or trigrams from the given text and returns the top N n-grams with their frequencies.

#### **Request Body**
| Field       | Type    | Default | Description                       |
|-------------|---------|---------|-----------------------------------|
| `text`      | `str`   | None    | Input text for processing.        |
| `ngram_size`| `int`   | `1`     | N-gram size (e.g., 1 for unigrams).|
| `top_n`     | `int`   | `10`    | Number of top results to return.  |

#### **Sample Input**
```json
{
   "text": "Mojo: Reels и Video Maker Videoleap: Видео от Lightricks",
   "ngram_size": 2,
   "top_n": 5
}
```

#### **Sample Output**
```json
{
   "ngram_size": 2,
   "top_ngrams": [
       {"phrase": "video maker", "count": 1},
       {"phrase": "reels video", "count": 1},
       {"phrase": "video от", "count": 1},
       {"phrase": "maker videoleap", "count": 1},
       {"phrase": "и video", "count": 1}
   ]
}
```

---

## **Features**

- **Dynamic N-gram Sizes**: Generate unigrams, bigrams, or trigrams using the `ngram_size` parameter.
- **Top Results**: Control the number of top results returned with the `top_n` parameter.
- **Interactive API Documentation**: Test and explore the API using Swagger UI.
- **Ready for Deployment**: Deploy on platforms like Heroku, AWS, or Docker.

---

## **Notes**

- Ensure you have installed the `ru_core_news_sm` language model for spaCy.
- The API can handle multiple languages by switching the spaCy language model.
- Extendable to support other NLP tasks like sentiment analysis, entity recognition, etc.
