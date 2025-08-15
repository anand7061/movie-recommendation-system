# # i have imported a library which name is streamlit
# import streamlit as st
# import pickle
# import pandas
# import requests
#
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=7da08d0d6d5045dd8b8175b6a3c07015&language=en-US".format(
#         movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     #tmdb path
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path
#
#
# #load the movie Dataframe
# movies = pickle.load(open('movie.pkl','rb')) #this should be a data frame
# similarity= pickle.load(open('similarity.pkl','rb'))
#
# def recommend(selected_movie):
#     #find index of the selected movie
#     movie_index = movies[movies['title']== selected_movie].index[0]
#     distances=similarity[movie_index]
#
#     #get top 5 similar movies (excluding itself)
#     movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
#
#     recommended_movie = []
#     recommended_movie_poster =[]
#
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         #fetch poster from API
#         # c833744415968ea168f9fd3b51b3e7
#
#         recommended_movie.append(movies.iloc[i[0]].movie_id)
#         recommended_movie_poster.append(fetch_poster(movie_id))
#     return recommended_movie,recommended_movie_poster
#
# # movie_list = pickle.load(open('movie.pkl','rb'))
# movie_list = movies['title'].values
#
#
# st.title('Movie recommender system')
# # streamlit run app.py
#
# # I have copy the code from streamlit API reference
#
# #For dropdown menu, we just pass the titles
#
# selected_movie_name= st.selectbox(
#     "Select a movie:",
#     movie_list
# )
#
# #for adding button we copy from API reference of code
# if st.button('Show Recommend'):
#     recommended_movie_names,recommended_movie_posters=recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.beta_columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#
#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])








import streamlit as st
import pickle
import pandas as pd
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --- CSS STYLING ---
def local_css():
    st.markdown("""
    <style>
    /* --- General Styles --- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
    }

    /* --- Main App Container --- */
    .stApp {
        background-color: #121212;
        color: #E5E4E2;
    }

    /* --- Title --- */
    h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #FFFFFF;
        text-align: center;
        padding-bottom: 20px;
    }

    /* --- Select Box --- */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #222222;
        border-color: #444444;
        color: #E5E4E2;
    }

    /* --- Button --- */
    .stButton > button {
        border: 2px solid #386120;
        border-radius: 20px;
        color: #386120;
        background-color: transparent;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: rgba(56, 97, 32, 0.5);
        color: #ffffff;
        border-color: #386124;
    }
    button[kind="secondary"], button[kind="primary"] {
    transition: transform 0.3s ease, background-color 0.3s ease;
}
button[kind="secondary"]:hover, button[kind="primary"]:hover {
    transform: scale(1.05);
    background-color: #4CAF50 !important;
}


    /* --- Recommendation Cards --- */
    .card {
        background-color: transparent;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%; /* Make cards in a row have the same height */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 16px rgba(0, 255, 255, 0.3);
    }
    .card-img {
        width: 100%;
        border-radius: 8px;
        margin-bottom: 10px;
        object-fit: cover;
    }
    .card-title {
        font-size: 16px;
        font-weight: 600;
        color: #E5E4E2;
    }
    .movie-title {
    font-family: 'Poppins', sans-serif;
    alignment: center;
    font-size: 20px;
    font-weight: 600;
    color: #ffffff; /* White text */
    text-align: center;
    margin-top: 8px;
}

    </style>
    """, unsafe_allow_html=True)


local_css()

# Function to fetch movie poster
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7da08d0d6d5045dd8b8175b6a3c07015&language=en-US"
#     try:
#         response = requests.get(url, timeout=5)  # 5 sec timeout
#         response.raise_for_status()  # Raise HTTPError for bad status
#         data = response.json()
#         poster_path = data.get('poster_path')
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#         else:
#             return None
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching poster: {e}")
#         return None

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7da08d0d6d5045dd8b8175b6a3c07015&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass  # Silently ignore any connection/API errors

    # Return placeholder image if something went wrong
    return "https://via.placeholder.com/500x750?text=No+Image"



# Load the DataFrame and similarity matrix
movies = pickle.load(open('movie.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to recommend movies
def recommend(selected_movie):
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        recommended_movie_posters.append(poster if poster else "https://via.placeholder.com/500x750?text=No+Image")

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
# st.title('🎬 Movie Recommender System')
st.markdown("<h1 style='text-align: center; color: #ffffff;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 2px solid #386120;'>", unsafe_allow_html=True)



movie_list = movies['title'].values
selected_movie_name = st.selectbox("Select a movie:", movie_list)

if st.button('Show Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        col.markdown(f"<p class='card-title'>{name}</p>", unsafe_allow_html=True)
        col.image(poster)






