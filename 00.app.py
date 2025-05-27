import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#df = pd.read_csv(r'C:\Users\admin\Music\Guvi\IMDb\merged_movies_sorted.csv')

@st.cache_data
def load_data():
    data = pd.read_csv("merged_movies_sorted.csv")
    return data

df = load_data()



# 1.Top 10 Movies by Rating and Voting Counts:
st.header("Top 10 Movies by Rating and Voting Counts (Grouped Bar Chart)")

top_movies = df.sort_values(by=['imdb_score', 'votes'], ascending=False).head(10)
titles = top_movies['title']
ratings = top_movies['imdb_score']
votes = top_movies['votes'] / 1000  # Scale down votes to align better with rating scale

x = np.arange(len(titles))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bar1 = ax.bar(x - width/2, ratings, width, label='IMDb Score')
bar2 = ax.bar(x + width/2, votes, width, label='Votes (x1000)')

ax.set_ylabel('Values')
ax.set_title('Top 10 Movies by IMDb Score and Votes')
ax.set_xticks(x)
ax.set_xticklabels(titles, rotation=45, ha='right')
ax.legend()

st.pyplot(fig)


# 2. Genre Distribution: (Animation, Adventure, Fantasy, Family)
st.header("Genre Distribution")
filtered_genres = df[df['genre'].isin(['Animation', 'Adventure', 'Fantasy', 'Family'])]
genre_counts = filtered_genres['genre'].value_counts()
st.bar_chart(genre_counts)

# 3. Average Duration by Genre:
st.header("Average Duration by Genre:")
genre_duration = filtered_genres.groupby('genre')['runtime'].mean()
st.bar_chart(genre_duration)

# 4. Voting Trends by Genre:
st.header("Voting Trends by Genre:")
genre_votes = df.groupby('genre')['votes'].mean().sort_values(ascending=False)
st.bar_chart(genre_votes.head(10))

# 5. Rating Distribution:
st.header("Rating Distribution:")
filtered_df = df[df['imdb_score'] > 0]  # 0 ரேட்டிங்கைத் தவிர்க்க
fig, ax = plt.subplots()
sns.histplot(filtered_df['imdb_score'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# 6. Genre-Based Rating Leaders:
st.header("Genre-Based Rating Leaders:")
top_genre_movies = filtered_genres.loc[filtered_genres.groupby('genre')['imdb_score'].idxmax()]
st.table(top_genre_movies[['genre', 'title', 'imdb_score']])

# 7. Most Popular Genres by Voting:
st.header("Most Popular Genres by Voting:")
genre_total_votes = df.groupby('genre')['votes'].sum().nlargest(5)

fig, ax = plt.subplots()
ax.pie(genre_total_votes, labels=genre_total_votes.index, autopct="%1.1f%%", startangle=90)
ax.set_title("Top 5 Genres by Total Votes")
ax.axis('equal')  # Ensures pie is drawn as a circle

st.pyplot(fig)


# 8. Duration Extremes:
st.header("Duration Extremes:")
duration_stats = df[['title', 'runtime']].sort_values('runtime')
st.table(pd.concat([duration_stats.head(3), duration_stats.tail(3)]))

# 9. Ratings by Genre:
st.header("Ratings by Genre (Heatmap Comparison)")

# Calculate average IMDb score per genre
genre_ratings = filtered_genres.groupby('genre')['imdb_score'].mean().sort_values(ascending=False)

# Reshape for a 1-row heatmap
heatmap_data = pd.DataFrame(genre_ratings).T  # Transpose to make genres columns

# Create heatmap
fig, ax = plt.subplots(figsize=(12, 2))  # Wide and short for a clean horizontal heatmap
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True, ax=ax)
ax.set_ylabel('')
ax.set_xlabel('Genre')
ax.set_title('Average IMDb Rating by Genre')

st.pyplot(fig)


# 10. Correlation Analysis:
st.header("Correlation Analysis:")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='imdb_score', y='votes', alpha=0.5, ax=ax)
st.pyplot(fig)
