# Movie Match

[![CI](https://github.com/ayusprasad/movie/actions/workflows/ci.yml/badge.svg)](https://github.com/ayusprasad/movie/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Recommender-FF4B4B?logo=streamlit&logoColor=white)
![TMDb](https://img.shields.io/badge/Posters-TMDb-01B4E4?logo=themoviedatabase&logoColor=white)

A Streamlit movie recommender that ranks similar titles from a precomputed similarity artifact and optionally loads posters from TMDb.

## Features

- Select a title from the bundled movie catalog.
- Rank similar titles using the local similarity matrix.
- Show poster artwork when a TMDb API key is configured.
- Continue to use recommendations when poster lookup is unavailable.

## Architecture

```text
Streamlit UI (app.py)
  ├─ movies.pkl       → title and movie ID catalog
  ├─ movie_dict.pkl   → precomputed similarity scores
  └─ TMDb API         → optional poster images
```

The pickled files are trusted local model artifacts. Replace them only with artifacts produced for this application.

## Tech stack

Python 3.11+, Streamlit, pandas, requests, TMDb API, pytest, Ruff, GitHub Actions.

## Run locally

### Prerequisites

- Python 3.11 or newer
- A TMDb API key for poster images (optional)

### Install

```bash
git clone https://github.com/ayusprasad/movie.git
cd movie
python -m venv .venv
```

Activate the environment:

- macOS/Linux: `source .venv/bin/activate`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Configure and start

Copy `.env.example` to `.env` and set `TMDB_API_KEY` if you want poster images. Recommendations work without this variable.

```bash
streamlit run app.py
```

Select a movie and choose **Show recommendations**. If poster retrieval fails, the titles remain available with a short poster status note.

## Quality checks

```bash
ruff check app.py tests
pytest -q
python -m compileall -q app.py tests
```

GitHub Actions runs the lint, unit tests, and compile checks for pushes and pull requests.

## Security

Keep API keys in local environment configuration and never commit them. Rotate any key that has already been committed; removing it from the current source does not remove it from Git history.
