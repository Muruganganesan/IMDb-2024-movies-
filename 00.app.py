import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#df = pd.read_csv(r'C:\Users\admin\Music\Guvi\IMDb\merged_movies_sorted.csv')

@st.cache_data
def load_data():
    data = pd.read_csv("merged_movies_sorted.csv")
    return data

df = load_data()



# 1.Top 10 Movies by Rating and Voting Counts:
st.header("Top 10 Movies by Rating and Voting Counts")
top_movies = df.sort_values(by=['imdb_score', 'votes'], ascending=False).head(10)
st.bar_chart(top_movies[['title', 'imdb_score', 'votes']].set_index('title'))

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
st.pyplot(genre_total_votes.plot.pie(autopct="%1.1f%%").figure)

# 8. Duration Extremes:
st.header("Duration Extremes:")
duration_stats = df[['title', 'runtime']].sort_values('runtime')
st.table(pd.concat([duration_stats.head(3), duration_stats.tail(3)]))

# 9. Ratings by Genre:
st.header("Ratings by Genre:")
genre_ratings = filtered_genres.groupby('genre')['imdb_score'].mean().reset_index()
heatmap_data = genre_ratings.pivot_table(index='genre', values='imdb_score')
fig, ax = plt.subplots()
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# 10. Correlation Analysis:
st.header("Correlation Analysis:")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='imdb_score', y='votes', alpha=0.5, ax=ax)
st.pyplot(fig)
