import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

@st.cache_data
def load_data():
    data = pd.read_csv("1.merged_movies_sorted.csv")
    return data

df = load_data()

st.title("IMDB 2024 Data visualization")

# Display Key Metrics
st.header("🎯 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Movies", value=f"{len(df):,}")

with col2:
    avg_score = df['imdb_score'].mean()
    st.metric(label="Average IMDb Score", value=f"{avg_score:.2f}")

with col3:
    highest_score = df['imdb_score'].max()
    st.metric(label="Highest IMDb Score", value=f"{highest_score:.1f}")
    
col4, col5, col6 = st.columns(3)

with col4:
    total_votes = df['votes'].sum()
    st.metric(label="Total Votes", value=f"{total_votes:,}")

with col5:
    longest_runtime = df['runtime'].max()
    st.metric(label="Longest Runtime (min)", value=f"{longest_runtime:.0f}")

with col6:
    shortest_runtime = df['runtime'].min()
    st.metric(label="Shortest Runtime (min)", value=f"{shortest_runtime:.0f}")



# 1.Top 10 Movies by Rating and Voting Counts:
st.header("1.Top 10 Movies by Voting Counts")
top_by_votes = df.sort_values(by='votes', ascending=False).head(10)
st.bar_chart(top_by_votes.set_index('title')['votes'])

st.header("Top 10 Movies by IMDb Score (Correct Bar Length)")

top_by_score = df.sort_values(by='imdb_score', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_by_score['title'], top_by_score['imdb_score'], color='mediumseagreen')
ax.set_xlabel('IMDb Score')
ax.set_title('Top 10 Movies by IMDb Score')
ax.invert_yaxis()  # Highest score on top

# Optional: Add score labels at end of bars
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f'{width:.1f}', va='center')

st.pyplot(fig)

# 2. Genre Distribution: (Animation, Adventure, Fantasy, Family)
st.header("2.Genre Distribution")
filtered_genres = df[df['genre'].isin(['Animation', 'Adventure', 'Fantasy', 'Family'])]
genre_counts = filtered_genres['genre'].value_counts()
st.bar_chart(genre_counts)

# 3. Average Duration by Genre:
st.header("3.Average Duration by Genre:")
genre_duration = filtered_genres.groupby('genre')['runtime'].mean()
st.bar_chart(genre_duration)

# 4. Voting Trends by Genre:
st.header("4.Voting Trends by Genre:")
genre_votes = df.groupby('genre')['votes'].mean().sort_values(ascending=False)
st.bar_chart(genre_votes.head(10))

# 5. Rating Distribution:
st.header("5.Rating Distribution:")
filtered_df = df[df['imdb_score'] > 0]  # 0 ரேட்டிங்கைத் தவிர்க்க
fig, ax = plt.subplots()
sns.histplot(filtered_df['imdb_score'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# 6. Genre-Based Rating Leaders:
st.header("6.Genre-Based Rating Leaders:")
top_genre_movies = filtered_genres.loc[filtered_genres.groupby('genre')['imdb_score'].idxmax()]
st.table(top_genre_movies[['genre', 'title', 'imdb_score']])

# 7. Most Popular Genres by Voting:
st.header("7.Most Popular Genres by Voting:")
genre_total_votes = df.groupby('genre')['votes'].sum().nlargest(5)

fig, ax = plt.subplots()
ax.pie(genre_total_votes, labels=genre_total_votes.index, autopct="%1.1f%%", startangle=90)
ax.set_title("Top 5 Genres by Total Votes")
ax.axis('equal')  # Ensures pie is drawn as a circle

st.pyplot(fig)


# 8. Duration Extremes:
st.header("8.Duration Extremes:")
duration_stats = df[['title', 'runtime']].sort_values('runtime')
st.table(pd.concat([duration_stats.head(3), duration_stats.tail(3)]))

# 9. Ratings by Genre:
st.header("9.Ratings by Genre (Heatmap Comparison)")

# Step 1: Split multi-genre strings and explode
df_genres = df.copy()
df_genres['genre'] = df_genres['genre'].str.split(',\s*')  # split by comma + optional space
df_exploded = df_genres.explode('genre')

# Step 2: Filter only the target genres
target_genres = ['Animation', 'Adventure', 'Fantasy', 'Family']
filtered_genres = df_exploded[df_exploded['genre'].isin(target_genres)]

# Step 3: Group by genre and compute average IMDb score
genre_ratings = filtered_genres.groupby('genre')['imdb_score'].mean().sort_values(ascending=False)

# Step 4: Create a 1-row heatmap
heatmap_data = pd.DataFrame(genre_ratings).T  # transpose
fig, ax = plt.subplots(figsize=(8, 2))
sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlGnBu", cbar=True, ax=ax)
ax.set_ylabel('')
ax.set_xlabel('Genre')
ax.set_title('Average IMDb Rating by Genre')

st.pyplot(fig)
st.dataframe(genre_ratings.round(3).reset_index().rename(columns={'genre': 'Genre', 'imdb_score': 'Avg IMDb Score'}))

# 10. Correlation Analysis:
st.header("10.Correlation Analysis:")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='imdb_score', y='votes', alpha=0.5, ax=ax)
st.pyplot(fig)
