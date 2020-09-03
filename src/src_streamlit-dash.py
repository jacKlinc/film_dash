import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache
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

st.title("Movie Dashboard")

# Runtime limits using sliders in sidebar
st.sidebar.markdown('### Runtime')  
runtime1 = st.sidebar.slider('Runtime lower limit', 0, movies.runtime.max(), 0, step=5)
runtime2 = st.sidebar.slider('Runtime upper limit', 0, movies.runtime.max(), movies.runtime.max(), step=5)

# Revenue limits using sliders in sidebar
st.sidebar.markdown('### Revenue')
revenue1 = st.sidebar.slider('Revenue lower limit', 0, movies.revenue.max(), 0, step=10000)
revenue2 = st.sidebar.slider('Revenue upper limit', 0, movies.revenue.max(), movies.revenue.max(), step=10000)

filtered = movies[
    (movies['runtime'] >= runtime1) & (movies['runtime'] < runtime2) &
    (movies['revenue'] >= revenue1) & (movies['revenue'] < revenue2)
]

'Control graph limits in the sidebar'
# Graph runtime vs revenue
sns.scatterplot(x='runtime', y='revenue', data=filtered)
st.pyplot()