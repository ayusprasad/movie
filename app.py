import os
import pickle
import requests
import streamlit as st
import pandas as pd
from generate_similarity import clean_tag


st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")

TMDB_API_KEY = "6817ef02392a699bf4501db1549f05e5"
PLACEHOLDER_POSTER = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&auto=format&fit=crop&q=60"


@st.cache_data(show_spinner=False)
def load_movie_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    movies_path = os.path.join(base_dir, 'movies.pkl')
    with open(movies_path, 'rb') as f:
        movies = pickle.load(f)
    return movies


@st.cache_resource(show_spinner=False)
def load_similarity_model(movies):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    top_indices_path = os.path.join(base_dir, 'top_similar_indices.pkl')
    similarity_path = os.path.join(base_dir, 'similarity.pkl')

    if os.path.exists(top_indices_path):
        with open(top_indices_path, 'rb') as f:
            return {'mode': 'top_indices', 'data': pickle.load(f)}

    if os.path.exists(similarity_path):
        with open(similarity_path, 'rb') as f:
            return {'mode': 'matrix', 'data': pickle.load(f)}

    # On-demand fallback computation
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    clean_tags = movies['tags'].apply(clean_tag)
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(clean_tags).toarray()
    sim = cosine_similarity(vectors)
    top_indices = np.argsort(sim, axis=1)[:, -11:-1][:, ::-1]

    with open(top_indices_path, 'wb') as f:
        pickle.dump(top_indices, f)

    return {'mode': 'top_indices', 'data': top_indices}


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception:
        pass
    return PLACEHOLDER_POSTER


def recommend(movie_title, movies, model):
    matches = movies[movies['title'] == movie_title]
    if matches.empty:
        return [], []

    idx = matches.index[0]
    names, posters = [], []

    if model['mode'] == 'top_indices':
        similar_indices = model['data'][idx][:5]
        for sim_idx in similar_indices:
            movie_id = movies.iloc[sim_idx].movie_id
            names.append(movies.iloc[sim_idx].title)
            posters.append(fetch_poster(movie_id))
    else:
        sim_matrix = model['data']
        distances = sorted(list(enumerate(sim_matrix[idx])), reverse=True, key=lambda x: x[1])
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            names.append(movies.iloc[i[0]].title)
            posters.append(fetch_poster(movie_id))

    return names, posters


movies = load_movie_data()
model = load_similarity_model(movies)

st.title("🎬 Movie Recommender System")
st.markdown("Content-based recommendation powered by TMDB metadata and cosine similarity.")

col_sel, _ = st.columns([2, 1])
with col_sel:
    movie_list = sorted(movies['title'].values)
    selected_movie = st.selectbox(
        "Choose a movie you like:",
        movie_list,
        index=movie_list.index("Avatar") if "Avatar" in movie_list else 0
    )

if st.button('✨ Show Similar Movies', type='primary'):
    with st.spinner("Finding best matches..."):
        names, posters = recommend(selected_movie, movies, model)

    if names:
        cols = st.columns(len(names))
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.caption(name)
                st.image(poster, use_container_width=True)
    else:
        st.warning("No recommendations found.")
