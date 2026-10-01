
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="MovieLens Dashboard",
    layout="wide"
)

st.title("MovieLens Dashboard")
st.write("Explore movie genres, ratings, release years, and highly rated movies.")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("./data/movie_ratings.csv")

# Make sure year is numeric
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# -----------------------------
# Split genres
# -----------------------------
genre_df = df.assign(
    genre=df["genres"].str.split("|")
).explode("genre")


# ============================================================
# 1. GENRE BREAKDOWN
# ============================================================
st.header("1. Genre Breakdown")

genre_counts = (
    genre_df.groupby("genre")["movie_id"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index(name="movie_count")
)

fig1 = px.bar(
    genre_counts,
    x="movie_count",
    y="genre",
    orientation="h",
    title="Distribution of Genres Among Rated Movies",
    labels={
        "movie_count": "Number of Rated Movies",
        "genre": "Genre"
    },
    hover_data={
        "movie_count": True
    }
)

fig1.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=600
)

st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# 2. GENRE SATISFACTION
# ============================================================
st.header("2. Genre Satisfaction")

selected_genres = st.multiselect(
    "Which genres would you like to explore?",
    sorted(genre_df["genre"].unique())
)

# Filter the data if genres were selected
if selected_genres:
    filtered_genre_df = genre_df[
        genre_df["genre"].isin(selected_genres)
    ]
else:
    filtered_genre_df = genre_df

genre_avg = (
    filtered_genre_df.groupby("genre")["rating"]
    .mean()
    .sort_values(ascending=False)
    .reset_index(name="average_rating")
)

fig2 = px.bar(
    genre_avg,
    x="average_rating",
    y="genre",
    orientation="h",
    title="Average Rating by Genre",
    labels={
        "average_rating": "Average Rating",
        "genre": "Genre"
    },
    hover_data={
        "average_rating": ":.2f"
    }
)

fig2.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis={"range": [0, 5]},
    height=600
)

st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# 3. RATINGS OVER TIME
# ============================================================
st.header("3. Ratings Over Time")

year_ratings = (
    df.groupby("year")["rating"]
    .mean()
    .sort_index()
    .reset_index(name="mean_rating")
)

fig3 = px.line(
    year_ratings,
    x="year",
    y="mean_rating",
    markers=True,
    title="Mean Movie Rating by Release Year",
    labels={
        "year": "Movie Release Year",
        "mean_rating": "Mean Rating"
    },
    hover_data={
        "year": True,
        "mean_rating": ":.2f"
    }
)

fig3.update_layout(
    height=600,
    xaxis=dict(
        tickmode="linear",
        dtick=5
    ),
    yaxis=dict(
        range=[0, 5]
    )
)

st.plotly_chart(fig3, use_container_width=True)


# ============================================================
# 4. BEST MOVIES
# ============================================================
st.header("4. Best Movies, With a Rating Floor")

# Calculate number of ratings and average rating per movie
movie_stats = (
    df.groupby(["movie_id", "title"])
    .agg(
        rating_count=("rating", "count"),
        average_rating=("rating", "mean")
    )
    .reset_index()
)

# Interactive threshold
threshold = st.selectbox(
    "Minimum number of ratings",
    [50, 150]
)

top_movies = (
    movie_stats[
        movie_stats["rating_count"] >= threshold
    ]
    .sort_values(
        "average_rating",
        ascending=False
    )
    .head(5)
)

# Reverse order so highest appears at top
plot_data = top_movies.sort_values("average_rating")

fig4 = px.bar(
    plot_data,
    x="average_rating",
    y="title",
    orientation="h",
    title=f"Top 5 Movies — At Least {threshold} Ratings",
    labels={
        "average_rating": "Average Rating",
        "title": "Movie"
    },
    hover_data={
        "average_rating": ":.2f",
        "rating_count": True
})

fig4.update_layout(
    xaxis={"range": [0, 5]},
    height=500
)

st.plotly_chart(fig4, use_container_width=True)

# Show the actual numbers underneath
st.dataframe(
    top_movies[
        ["title", "average_rating", "rating_count"]
    ].rename(
        columns={
            "title": "Movie",
            "average_rating": "Average Rating",
            "rating_count": "Number of Ratings"
        }
    ),
    hide_index=True,
    use_container_width=True
)