# 🎬 Movie Recommender System

A content-based movie recommender web application built with **Python**, **Streamlit**, and **scikit-learn**, utilizing TMDB 5000 movie metadata and cosine similarity metrics.

![Movie Recommender](https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1200&auto=format&fit=crop&q=80)

## Features
- **Smart Recommendations:** Recommends 5 relevant movies based on genre, plot keywords, cast, and director metadata.
- **Dynamic TMDB Posters:** Fetches high-resolution movie posters directly from TMDB API with placeholder fallbacks.
- **Compact & Deployable Model:** Optimized from raw 185 MB dense similarity matrix to a compact index lookup (`top_similar_indices.pkl`) allowing instant startup and seamless deployment on free tiers (Streamlit Cloud, Render, Hugging Face Spaces).
- **Dockerized:** Fully containerized with a slim production image.

---

## Quickstart

### 1. Local Run
```bash
# Clone repository
git clone https://github.com/ayusprasad/movie.git
cd movie

# Install dependencies
pip install -r requirements.txt

# (Optional) Rebuild index if modifying tags
python generate_similarity.py

# Launch Streamlit app
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### 2. Run with Docker
```bash
# Build Docker image
docker build -t movie-recommender .

# Run container
docker run -p 8501:8501 movie-recommender
```
Open [http://localhost:8501](http://localhost:8501).

---

## Project Structure
```text
movie/
├── app.py                     # Streamlit application entrypoint
├── generate_similarity.py     # Vectorizer & index pre-computation
├── movies.pkl                 # TMDB movies metadata dataframe
├── movie_dict.pkl             # Dictionary format of movies
├── top_similar_indices.pkl    # Pre-calculated top-10 similarity index
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Production container definition
└── README.md                  # Project documentation
```
