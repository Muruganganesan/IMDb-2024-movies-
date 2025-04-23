import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load Data
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: Could not find the file at {file_path}. Please check the file path.")
        return None

file_path = 'merged_movies_sorted.csv'
movies_df = load_data(file_path)

if movies_df is not None:
    # Title
    st.title('IMDb Movies Dashboard')

    # Sidebar Filters
    st.sidebar.header('Filters')

    # Genre Filter
    genres = movies_df['genre'].unique().tolist()
    genre_filter = st.sidebar.multiselect('Select Genre(s)', genres, default=genres)

    # Year Slider
    min_year = int(movies_df['runtime'].min())
    max_year = int(movies_df['runtime'].max())
    year_range = st.sidebar.slider('Select your Duration', min_year, max_year, (min_year, max_year))

    # Search Box
    search_term = st.sidebar.text_input('Search Movie Title')

    # Filter Data
    filtered_df = movies_df[movies_df['genre'].isin(genre_filter)]
    filtered_df = filtered_df[
        (filtered_df['runtime'] >= year_range[0]) & (filtered_df['runtime'] <= year_range[1])
    ]
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_term, case=False)]

    # Movie Data Table
    st.subheader('Filtered Movies Data')
    st.dataframe(filtered_df[['title', 'runtime', 'imdb_score', 'votes', 'genre']])

    # IMDb Score Distribution Histogram
    st.subheader('IMDb Score Distribution')
    fig = px.histogram(filtered_df, x='imdb_score', nbins=20, title='IMDb Score Distribution')
    st.plotly_chart(fig)

    # Votes Distribution Histogram
    st.subheader('Votes Distribution')
    fig2 = px.histogram(filtered_df, x='votes', nbins=20, title='Votes Distribution')
    st.plotly_chart(fig2)

    # Movie Titles Wordcloud
    st.subheader('Wordcloud of Movie Titles')
    text = ' '.join(filtered_df['title'].dropna().tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Key Metrics
    st.subheader('Key Metrics')
    col1, col2, col3 = st.columns(3)
    col1.metric('Total Movies', len(filtered_df))
    col2.metric('Average IMDb Score', round(filtered_df['imdb_score'].mean(), 2))
    col3.metric('Average Votes', int(filtered_df['votes'].mean()))

    # Footer
    st.markdown('---')
    st.markdown('Created by Murugan for the IMDb movie dataset.')
