import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=6817ef02392a699bf4501db1549f05e5&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')
st.image(
    'https://th.bing.com/th/id/R.b4da7e463ae0ae869f01c856a2d8eed2?rik=dBULFXpoQCYaVQ&riu=http%3a%2f%2f1.bp.blogspot.com%2f-HFt4m72Bge0%2fUOGuwboY9fI%2fAAAAAAAAAcc%2f8MwqSm9V8Fc%2fs1600%2f2012%2bMovies%2bCollage.jpg&ehk=ZA2xAdgxlD2ZbsAJZfqbqaK71%2fWAlATNa4H1qUfoLf8%3d&risl=&pid=ImgRaw&r=0')
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Select Your Favorite Movie",
    movie_list
)

if st.button('Show Similear Movies'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
