import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache()
def get_movies():
    movie_ratings = pd.read_csv('./data/movies_metadata.csv', usecols=['revenue', 'runtime'])
    # Update data types
    movie_ratings = movie_ratings.convert_dtypes()
    # Drop missing values
    movie_ratings.dropna(inplace=True)
    # Drop zeros for revenue
    movie_ratings.drop(movie_ratings[movie_ratings.revenue == 0].index, inplace=True)
    # Drop zeros for runtime
    movie_ratings.drop(movie_ratings[movie_ratings.runtime == 0].index, inplace=True)

    return movie_ratings

movies = get_movies()

# Show top movies
st.dataframe(movies.head())

# Graph runtime vs revenue
sns.scatterplot(x='runtime', y='revenue', data=movies)
st.pyplot()