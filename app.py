
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Page setup
# -------------------------

st.set_page_config(
    page_title="MovieLens Dashboard",
    layout="wide"
)

st.title("MovieLens Dashboard")

# Load data
df = pd.read_csv("./data/movie_ratings.csv")

df["year"] = pd.to_numeric(df["year"], errors="coerce")


# -------------------------
# Question 1
# -------------------------

st.header("1. Genre Breakdown")

genre_df = df.assign(
    genre=df["genres"].str.split("|")
).explode("genre")

genre_counts = (
    genre_df.groupby("genre")["movie_id"]
    .nunique()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 6))

genre_counts.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_xlabel("Number of Rated Movies")
ax.set_ylabel("Genre")
ax.set_title("Distribution of Genres Among Rated Movies")

st.pyplot(fig)


# -------------------------
# Question 2
# -------------------------

st.header("2. Genre Satisfaction")


genre_avg = (
    genre_df.groupby("genre")["rating"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 6))

genre_avg.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_xlabel("Average Rating")
ax.set_ylabel("Genre")
ax.set_title("Average Rating by Genre")

st.pyplot(fig)


# -------------------------
# Question 3
# -------------------------

st.header("3. Ratings Over Time")

year_ratings = (
    df.groupby("year")["rating"]
    .mean()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(12, 6))

year_ratings.plot(
    kind="line",
    ax=ax
)

ax.set_xlabel("Movie Release Year")
ax.set_ylabel("Mean Rating")
ax.set_title("Mean Movie Rating by Release Year")

st.pyplot(fig)


# -------------------------
# Question 4
# -------------------------

st.header("4. Best Movies")

movie_stats = (
    df.groupby(["movie_id", "title"])
    .agg(
        rating_count=("rating", "count"),
        average_rating=("rating", "mean")
    )
    .reset_index()
)

threshold = st.selectbox(
    "Minimum number of ratings",
    [50, 150]
)

top_movies = (
    movie_stats[movie_stats["rating_count"] >= threshold]
    .sort_values("average_rating", ascending=False)
    .head(5)
)

st.dataframe(top_movies)

fig, ax = plt.subplots(figsize=(10, 6))

plot_data = top_movies.sort_values("average_rating")

ax.barh(
    plot_data["title"],
    plot_data["average_rating"]
)

ax.set_xlabel("Average Rating")
ax.set_ylabel("Movie")
ax.set_title(
    f"Top 5 Movies — At Least {threshold} Ratings"
)

st.pyplot(fig)