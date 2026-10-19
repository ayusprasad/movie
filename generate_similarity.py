import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_tag(t):
    words = [w.replace(' ', '') for w in str(t).split('   ')]
    return ' '.join(w for w in words if w)


def build_and_save_similarity(movies_pkl_path='movies.pkl', output_path='top_similar_indices.pkl'):
    """
    Computes top-10 recommended movie indices for all 4806 movies.
    Saving top indices instead of full 4806x4806 float matrix reduces file size from 185MB to ~190KB,
    allowing it to be pushed to GitHub cleanly and loaded instantly on free tiers.
    """
    if not os.path.exists(movies_pkl_path):
        raise FileNotFoundError(f"{movies_pkl_path} not found.")

    print(f"Loading {movies_pkl_path}...")
    movies = pickle.load(open(movies_pkl_path, 'rb'))
    clean_tags = movies['tags'].apply(clean_tag)

    print("Vectorizing tags...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(clean_tags).toarray()

    print("Computing cosine similarity...")
    sim = cosine_similarity(vectors)

    print("Extracting top 10 similar indices per movie...")
    # top 10 indices (excluding self at index 0)
    top_indices = np.argsort(sim, axis=1)[:, -11:-1][:, ::-1]

    with open(output_path, 'wb') as f:
        pickle.dump(top_indices, f)

    print(f"Successfully generated {output_path} ({os.path.getsize(output_path) / 1024:.1f} KB).")
    return top_indices


if __name__ == '__main__':
    build_and_save_similarity()
