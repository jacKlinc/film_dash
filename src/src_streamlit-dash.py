import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Turn JSON into list of genres
def make_list(row):
    j=[]
    for i in row:
        j.append(i['name'])
    return j

# Get each genre of each row and write to list
def get_unique(row):
    for i in row:
        return i['name']

st.title("Movie Dashboard")

@st.cache(allow_output_mutation=True)
def load_data():
    usecols=['budget', 'genres', 'original_language', 
         'production_companies', 'production_countries', 'release_date', 
         'revenue', 'runtime', 'spoken_languages', 'title', 'vote_average', 'vote_count']

    used_dtypes = {
        "genres": object, 
        "original_language": str, 
        "production_companies": object,  
        "production_countries": object, 
        "release_date": str, 
        "spoken_languages": object, 
        "title": str, 
        "vote_average": float,
        "vote_count": float
    }

    movies = pd.read_csv('./data/movies_metadata.csv', dtype=used_dtypes, usecols=usecols)
    # movies = movies[['id','imdb_id','title','budget','genres','original_language','production_countries','release_date','revenue','runtime','status','vote_average','vote_count']]
    movies = movies.convert_dtypes()

    # Parse dates
    movies.release_date = pd.to_datetime(movies.release_date, format='%Y-%m-%d', errors='coerce')
    # Drop zeros for revenue & runtime
    movies.drop(movies[movies.revenue == 0].index, inplace=True)
    movies.drop(movies[movies.runtime == 0].index, inplace=True)

    # Replace single quotes with double and read as JSON
    movies.genres = movies.genres.apply(lambda a: json.loads(a.replace("'", "\"")))
    movies.genres.fillna('', inplace=True)

    return movies

movies = load_data()

## Runtime/Revenue Sliders
# Runtime limits using sliders in sidebar
st.sidebar.markdown('### Runtime')  
runtime1 = st.sidebar.slider('Runtime lower limit', 0, movies.runtime.max(), 0, step=5)
runtime2 = st.sidebar.slider('Runtime upper limit', 0, movies.runtime.max(), movies.runtime.max(), step=5)

# Revenue limits using sliders in sidebar
st.sidebar.markdown('### Revenue')
revenue1 = st.sidebar.slider('Revenue lower limit', 0, movies.revenue.max(), 0, step=10000)
revenue2 = st.sidebar.slider('Revenue upper limit', 0, movies.revenue.max(), movies.revenue.max(), step=10000)


## Genre
st.sidebar.markdown('### Genre')
# Get unique list of genres
genre_list = pd.Series(list(map(get_unique, movies.genres))).unique()
# Convert JSON into list
movies['parsed_genres'] = pd.Series(list(map(make_list, movies.genres)))

# Convert to list and add Any option to slider
genre_list = genre_list.tolist()
genre_list.insert(0, 'Any')

# picked_genre = st.sidebar.selectbox(
#      'Pick a genre',
#      genre_list)

# # Remove other genre option
# genre_list = np.delete(genre_list, np.argwhere(genre_list == picked_genre))

# picked_genre2 = st.sidebar.selectbox(
#      'Pick another?',
#      genre_list)

# # Set to wildcard if either is 'Any
# picked_genre = picked_genre2 = '' if (picked_genre == 'Any') or (picked_genre2 == 'Any') else picked_genre

## Year slider
agree = st.sidebar.checkbox('Select year')

picked_year=''

if agree:
    st.sidebar.markdown('### Year')
    picked_year = st.sidebar.slider('Choose year', movies.release_date.min().year, movies.release_date.max().year, 2000)


if picked_year != '':
    filtered = movies[
        (movies.runtime >= runtime1) & (movies.runtime < runtime2) & 
        (movies.revenue >= revenue1) & (movies.revenue < revenue2) &
        # (movies.parsed_genres.str.contains(picked_genre, regex=False)) &
        # (movies.parsed_genres.str.contains(picked_genre2, regex=False)) &     
        (movies.release_date.dt.year == picked_year)
    ]
else:
    filtered = movies[
        (movies.runtime >= runtime1) & (movies.runtime < runtime2) & 
        (movies.revenue >= revenue1) & (movies.revenue < revenue2)
        # (movies.parsed_genres.str.contains(picked_genre, regex=False)) &
        # (movies.parsed_genres.str.contains(picked_genre2, regex=False))
    ]

# filtered = movies[
#     (movies.runtime >= runtime1) & (movies.runtime < runtime2) & 
#     (movies.revenue >= revenue1) & (movies.revenue < revenue2)
# ]
# if picked_year != '':
#     filtered = filtered & movies[ (movies.release_date.dt.year == picked_year) ]
    
# if picked_genre != '':
#     filtered = filtered & movies[ (movies.parsed_genres.str.contains(picked_genre, regex=False)) ]

# if picked_genre2 != '':
#     filtered = filtered & movies[ (movies.parsed_genres.str.contains(picked_genre2, regex=False)) ]
     

'Control graph limits in the sidebar'
# Graph runtime vs revenue
sns.scatterplot(x='runtime', y='revenue', data=filtered)
st.pyplot()