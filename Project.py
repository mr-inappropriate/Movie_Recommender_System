import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "5c39ab43b32181a1e3f1032404317c03"

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/150?text=No+Poster"
    except:
        return "https://via.placeholder.com/150?text=Error"


def recommend(movie_title):
    index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []
    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters


st.title('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie to get recommendations:", movie_list)

if st.button('Show Recommendations'):
    titles, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(titles[i])
            st.image(posters[i])
