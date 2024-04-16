import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=86096e21b77b53ef5152be0c1426f2d6')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']  # corrected 'poster_path'

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommendation System')
selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values)

# Assuming movies_dict is your dictionary loaded from 'movie_dict.pkl'
# Create an ID column starting from 1
for idx, title in enumerate(movies_dict.keys(), start=1):
    movies_dict[title]['movie_id'] = idx

def recommend(selected_movie_name):
    # Find the index of the selected movie in the DataFrame
    movie_index = movies[movies['title'] == selected_movie_name].index[0]

    # Get similarity scores for the selected movie
    similarities = similarity[movie_index]

    # Sort the movies by similarity and get the top 5 recommendations
    recommended_movies_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[1:6]

    recommended_movies = movies.iloc[recommended_movies_indices]['title'].tolist()
    recommended_movies_posters = [fetch_poster(movies.loc[index, 'movie_id']) for index in recommended_movies_indices]

    return recommended_movies, recommended_movies_posters


similarity = pickle.load(open('similarity.pkl', 'rb'))

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    num_columns = 5  # Number of columns for display
    num_movies = len(names)
    num_rows = -(-num_movies // num_columns)  # Ceiling division to calculate the number of rows

    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            index = i * num_columns + j
            if index < num_movies:
                with cols[j]:
                    st.write(names[index])
                    st.image(posters[index], width=200, use_column_width=True)  # Adjust the width of the image as needed
                    st.write("  ")  # Add empty space
            else:
                cols[j].write("")  # Write an empty string to create a placeholder column
