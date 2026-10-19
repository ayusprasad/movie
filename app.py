from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Any

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent
MOVIES_PATH = ROOT / "movies.pkl"
SIMILARITY_PATH = ROOT / "movie_dict.pkl"
POSTER_FALLBACK = "https://placehold.co/500x750?text=Poster+unavailable"


def recommend_movies(
    movies: pd.DataFrame,
    similarity: Any,
    selected_title: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Return the highest-scoring titles other than the selected movie."""
    required_columns = {"title", "movie_id"}
    if not required_columns.issubset(movies.columns):
        raise ValueError("The movie catalog must include title and movie_id columns.")

    catalog = movies.reset_index(drop=True)
    matches = catalog.index[catalog["title"].astype(str) == selected_title].tolist()
    if not matches:
        raise ValueError(f"Movie not found in the catalog: {selected_title}")
    if len(similarity) != len(catalog):
        raise ValueError("The similarity artifact does not match the movie catalog.")

    selected_index = matches[0]
    scores = similarity[selected_index]
    ranked = sorted(enumerate(scores), key=lambda item: float(item[1]), reverse=True)
    recommendations = []
    for index, score in ranked:
        if index == selected_index:
            continue
        row = catalog.iloc[index]
        recommendations.append(
            {
                "title": str(row["title"]),
                "movie_id": row["movie_id"],
                "score": float(score),
            }
        )
        if len(recommendations) >= max(0, limit):
            break
    return recommendations


def load_assets() -> tuple[pd.DataFrame, Any]:
    """Load the tracked movie catalog and similarity artifact."""
    if not MOVIES_PATH.is_file():
        raise FileNotFoundError(f"Movie catalog not found: {MOVIES_PATH.name}")
    if not SIMILARITY_PATH.is_file():
        raise FileNotFoundError(f"Similarity artifact not found: {SIMILARITY_PATH.name}")

    with MOVIES_PATH.open("rb") as movie_file:
        movies = pickle.load(movie_file)
    with SIMILARITY_PATH.open("rb") as similarity_file:
        similarity = pickle.load(similarity_file)

    if not isinstance(movies, pd.DataFrame):
        raise ValueError("movies.pkl must contain a pandas DataFrame.")
    if len(similarity) != len(movies):
        raise ValueError("The similarity artifact does not match the movie catalog.")
    return movies, similarity


def fetch_poster(movie_id: int | str, api_key: str) -> str | None:
    """Fetch a poster URL from TMDb; return None when no poster is available."""
    if not api_key:
        return None
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": api_key, "language": "en-US"},
            timeout=(3, 10),
        )
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
    except (requests.RequestException, ValueError):
        return None
    if not poster_path:
        return None
    return f"https://image.tmdb.org/t/p/w500{poster_path}"


@st.cache_resource
def _cached_assets() -> tuple[pd.DataFrame, Any]:
    return load_assets()


def main() -> None:
    st.set_page_config(page_title="Movie Match", page_icon="🎬")
    st.title("Movie Match")
    st.caption("Find films with a similar profile from the bundled catalog.")

    try:
        movies, similarity = _cached_assets()
    except (OSError, pickle.PickleError, EOFError, ImportError, ValueError) as error:
        st.error(f"The recommendation catalog could not be loaded: {error}")
        st.info("Confirm that movies.pkl and movie_dict.pkl are present and were generated together.")
        st.stop()

    titles = movies["title"].dropna().astype(str).tolist()
    if not titles:
        st.warning("The movie catalog is empty.")
        return

    selected_title = st.selectbox("Choose a movie", titles)
    if not st.button("Show recommendations", type="primary"):
        return

    try:
        recommendations = recommend_movies(movies, similarity, selected_title)
    except (TypeError, ValueError, IndexError) as error:
        st.error(f"Recommendations are unavailable: {error}")
        return

    if not recommendations:
        st.info("There are no other titles available to recommend.")
        return

    api_key = os.getenv("TMDB_API_KEY", "").strip()
    columns = st.columns(len(recommendations))
    for column, movie in zip(columns, recommendations):
        with column:
            poster_url = fetch_poster(movie["movie_id"], api_key)
            st.image(poster_url or POSTER_FALLBACK, use_container_width=True)
            st.markdown(f"**{movie['title']}**")


if __name__ == "__main__":
    main()
