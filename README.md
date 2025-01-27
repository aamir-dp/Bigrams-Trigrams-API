# **NLP API Documentation**

## **Overview**

This API processes a given text to generate **unigrams**, **bigrams**, **trigrams**, or higher-order n-grams, and returns the most frequently occurring n-grams with their counts. It is implemented using **FastAPI**, which offers a fast and interactive API experience.

---

## **Installation**

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn nltk
   ```

2. **Download Required NLTK Resources**:
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

3. **Save the API Code**:
   Save the provided Python script as `api.py`.

---

## **Running the API**

1. **Start the Server**:
   Run the following command in the terminal:
   ```bash
   uvicorn api:app --reload
   ```

2. **Access the Documentation**:
   Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view and interact with the API using the built-in Swagger UI.

---

## **Endpoints**

### **POST /ngrams**

#### **Description**
Generates n-grams (unigrams, bigrams, trigrams, etc.) from the given text and returns the top N n-grams with their frequencies.

#### **Request Body**
| Field        | Type    | Default | Description                                    |
|--------------|---------|---------|------------------------------------------------|
| `text`       | `str`   | None    | Input text for processing.                     |
| `ngram_size` | `int`   | `1`     | N-gram size (e.g., 1 for unigrams, 2 for bigrams). |

#### **Sample Input**
```json
{
   "text": "InShot - Video Editor\nSplice - Video Editor & Maker",
   "ngram_size": 2
}
```

#### **Sample Output**
```json
{
   "ngram_size": 2,
   "keywords": [
       {"keyword": "video editor", "count": 2},
       {"keyword": "splice video", "count": 1},
       {"keyword": "editor maker", "count": 1}
   ]
}
```

---

## **Features**

- **Dynamic N-gram Sizes**: Generate unigrams, bigrams, trigrams, or higher n-grams using the `ngram_size` parameter.
- **Interactive Documentation**: Easily test and explore the API using Swagger UI.
- **Lightweight and Flexible**: No external models like spaCy are required; uses only NLTK for processing.
- **Ready for Deployment**: Can be deployed on platforms like Heroku, Vercel, Render, or AWS.

---

## **Frontend Integration**

The API can be integrated with a frontend web interface to allow users to input text and visualize the generated n-grams. The following files are provided:

- **HTML**: `index.html`
- **CSS**: `styles.css`
- **JavaScript**: `script.js`

Ensure the `script.js` file points to the correct API endpoint URL.

---

## **Notes**

- Ensure you have Python 3.8 or above installed.
- Use `uvicorn` to run the server locally.
- CORS middleware is enabled to support cross-origin requests from a frontend application.
- For large text inputs, the API will process efficiently but may limit results to the top 20 n-grams for clarity.
