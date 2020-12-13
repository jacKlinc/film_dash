import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# kaggle api call
from src_kaggle_api_dataset import get_kaggle_dataset

# Turn JSON into list of genres
# def make_list(row):
#     j=[]
#     for i in row:
#         j.append(i['name'])
#     return j

# Get each genre of each row and write to list
# def get_unique(row):
#     i = []
#     i.append(row.replace('|',''))
#     return i

st.title("Movie Dashboard")

@st.cache(allow_output_mutation=True)
def load_data():
    usecols=['budget', 'genres', 'language', 
        #  'production_companies', 
         'country', 'title_year', 
         'gross', 'duration', 'language', 'movie_title', 'imdb_score', 'num_voted_users']

    used_dtypes = {
        "genres": object, 
        "language": str, 
        # "production_companies": object,  
        "country": object, 
        "title_year": str, 
        "spoken_languages": object, 
        "movie_title": str, 
        "imdb_score": float,
        "num_voted_users": float
    }

    # get dataset
    movies = get_kaggle_dataset('karrrimba/movie-metadatacsv', 'movie_metadata.csv', used_dtypes, usecols)

    # movies = pd.read_csv(dataset, dtype=used_dtypes, usecols=usecols)
    # movies = movies[['id','imdb_id','title','budget','genres','original_language','production_countries','title_year','gross','duration','status','vote_average','vote_count']]
    movies = movies.convert_dtypes()

    # Parse dates
    # movies.title_year = pd.to_datetime(movies.title_year, format='%Y-%m-%d', errors='coerce')
    # Drop zeros for gross & duration
    movies.drop(movies[movies.gross == 0].index, inplace=True)
    movies.drop(movies[movies.duration == 0].index, inplace=True)
    # movies.drop(movies[movies.title_year == 0].index, inplace=True)
    # movies.dropna(inplace=True)
    movies.title_year = movies.title_year.astype('int', errors='ignore')

    # Replace single quotes with double and read as JSON
    # movies.genres = movies.genres.apply(lambda a: json.loads(a.replace("'", "\"")))
    movies.genres.fillna('', inplace=True)

    return movies

movies = load_data()

## duration/gross Sliders
# duration limits using sliders in sidebar
st.sidebar.markdown('### duration')  
duration1 = st.sidebar.slider('duration lower limit', 0, int(movies.duration.max()), 0, step=5)
duration2 = st.sidebar.slider('duration upper limit', 0, int(movies.duration.max()), int(movies.duration.max()), step=5)

# gross limits using sliders in sidebar
st.sidebar.markdown('### gross')
gross1 = st.sidebar.slider('gross lower limit', 0, int(movies.gross.max()), 0, step=10000)
gross2 = st.sidebar.slider('gross upper limit', 0, int(movies.gross.max()), int(movies.gross.max()), step=10000)


## Genre
# st.sidebar.markdown('### Genre')
# Get unique list of genres
# genre_list = pd.Series(map(get_unique, movies.genres)).unique()
# Convert JSON into list
# movies['parsed_genres'] = pd.Series(list(map(make_list, movies.genres)))

# Convert to list and add Any option to slider
# genre_list = genre_list.tolist()
# genre_list.insert(0, 'Any')

## Year slider
# agree = st.sidebar.checkbox('Select year')

picked_year=''

# if agree:
#     st.sidebar.markdown('### Year')
#     picked_year = st.sidebar.slider('Choose year', int(movies.title_year.min()), int(movies.title_year.max()), 2000)
#     '', picked_year, type(picked_year)
#     '', movies.title_year[0], type(movies.title_year[0])


if picked_year != '':
    filtered = movies[
        (movies.duration >= duration1) & (movies.duration < duration2) & 
        (movies.gross >= gross1) & (movies.gross < gross2) &
        # (movies.parsed_genres.str.contains(picked_genre, regex=False)) &
        # (movies.parsed_genres.str.contains(picked_genre2, regex=False)) &     
        (movies.title_year == picked_year)
    ]
else:
    filtered = movies[
        (movies.duration >= duration1) & (movies.duration < duration2) & 
        (movies.gross >= gross1) & (movies.gross < gross2)
        # (movies.parsed_genres.str.contains(picked_genre, regex=False)) &
        # (movies.parsed_genres.str.contains(picked_genre2, regex=False))
    ]     

'Control graph limits in the sidebar'
# Graph duration vs gross
fig, ax = plt.subplots()
sns.scatterplot(x='duration', y='gross', data=filtered)
st.pyplot(fig)

# '## Recommender'
# 'Look for a movie you like'

# movie_search = st.text_input('Search for a movie')
# 'favourite movie: ', movie_search


# if movie_search:
#     'titles'
#     movies[movies.movie_title.str.contains(movie_search, case=False, regex=False, na=False)]


# 'Here\'s some you might like'