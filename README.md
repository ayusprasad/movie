# movie

Movie Recommender System

Overview

The Movie Recommender System is a Python-based application built using Streamlit. This application allows users to select their favorite movie and get recommendations for similar movies, complete with their posters, based on a machine learning similarity model. It leverages movie data from The Movie Database (TMDb) API for fetching movie posters.

Features

Interactive Movie Selection: Users can choose a movie from a list of available titles.

Recommendation Engine: Provides five movie recommendations similar to the selected movie.

Visual Appeal: Displays movie posters alongside their titles for an enhanced user experience.

Requirements

Libraries:

streamlit

pandas

pickle

requests

Files:

movies.pkl: A serialized file containing movie data, including titles and IDs.

similarity.pkl: A serialized file containing a precomputed similarity matrix for the movies.

Installation

Clone this repository:

git clone <repository_url>

Navigate to the project directory:

cd movie-recommender-system

Install the required libraries:

pip install streamlit pandas requests

Usage

Start the Streamlit application:

streamlit run app.py

Open the application in your browser (usually at http://localhost:8501).

Select a movie from the dropdown menu and click on the "Show Similar Movies" button.

View the recommendations and their posters.

How It Works

Data Loading:

The application loads movie data (movies.pkl) and a similarity matrix (similarity.pkl).

User Interaction:

The user selects a movie from a dropdown list.

Recommendation Engine:

Based on the selected movie, the application retrieves the most similar movies using the precomputed similarity matrix.

Poster Fetching:

The TMDb API is used to fetch posters for the recommended movies.

Display:

Recommendations, including titles and posters, are displayed in a visually appealing layout.

API Usage

The application uses TMDb API to fetch movie posters. Ensure you have an active TMDb API key and replace the placeholder in the code (6817ef02392a699bf4501db1549f05e5) with your own API key.

Example

When a user selects the movie "Inception," the application might suggest similar movies such as "Interstellar," "The Dark Knight," "Shutter Island," etc., with their posters displayed alongside their titles.

Acknowledgements

The Movie Database (TMDb) for providing movie data and poster images.

Streamlit for an easy-to-use framework for building interactive web applications.

Future Improvements

Add a search bar for faster movie selection.

Enhance the similarity algorithm for more accurate recommendations.

Include additional movie details such as genres and ratings.

Optimize performance for large datasets.

License

This project is licensed under the MIT License. See the LICENSE file for details.
