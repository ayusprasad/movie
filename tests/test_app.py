import pandas as pd
import pytest

from app import recommend_movies


@pytest.fixture
def catalog():
    return pd.DataFrame(
        [
            {"title": "Arrival", "movie_id": 1},
            {"title": "Contact", "movie_id": 2},
            {"title": "Interstellar", "movie_id": 3},
            {"title": "Gravity", "movie_id": 4},
        ]
    )


def test_recommend_movies_ranks_similar_titles_and_excludes_selection(catalog):
    similarity = [
        [1.0, 0.9, 0.8, 0.2],
        [0.9, 1.0, 0.1, 0.3],
        [0.8, 0.1, 1.0, 0.7],
        [0.2, 0.3, 0.7, 1.0],
    ]

    result = recommend_movies(catalog, similarity, "Arrival", limit=2)

    assert [movie["title"] for movie in result] == ["Contact", "Interstellar"]
    assert all(movie["title"] != "Arrival" for movie in result)


def test_recommend_movies_rejects_unknown_title(catalog):
    with pytest.raises(ValueError, match="not found"):
        recommend_movies(catalog, [[1, 0, 0, 0]] * 4, "Unknown")


def test_recommend_movies_checks_artifact_size(catalog):
    with pytest.raises(ValueError, match="does not match"):
        recommend_movies(catalog, [[1, 0]], "Arrival")
