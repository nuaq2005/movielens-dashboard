## Prompt Used

Using the following csv with these fields, how to create charts answering the following questions using pandas, python, etc. Then give instuctions on how to upload to streamlit * movie_ratings.csv — contains userId, movieId, rating, timestamp, title, year, and pipe-separated genres

**Question 1 — Genre Breakdown:** What's the distribution of genres among the movies that were rated? (Movies can have multiple genres — have the AI explain how it handled that before it counts anything.) 

**Question 2 — Genre Satisfaction:** Which genres have the highest average rating? Which have the lowest? 

**Question 3 — Ratings Over Time:** How has the mean rating changed across movie release years? 

**Question 4 — Best Movies, With a Floor:** What are the top 5 best-rated movies, once you only count movies with at least 50 ratings? What changes if you raise that floor to 150?

### Clarifying Prompts

I would like to divide the genres by the pipe seperation into individual genres rather than reading the pipe seperated genres as one string