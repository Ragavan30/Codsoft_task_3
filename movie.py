import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the dataset
data = pd.read_csv("C:/Users/RAGAVI/Downloads/movie.csv/1950-1989/bollywood_meta_1950-1989.csv", low_memory=False)
# Limiting to the first 20,000 rows
data = data.head(20000)

# Fill missing overviews with an empty string
data['overview'] = data['overview'].fillna('')

# Vectorize the 'overview' column
vectorizer = TfidfVectorizer(stop_words='english')
x = vectorizer.fit_transform(data['overview'])

# Create a DataFrame from the TF-IDF matrix
df = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names_out())

# Mapping of movie titles to their indices
indices = pd.Series(data.index, index=data['title']).drop_duplicates()

# Movie title input by the user
user_title = 'Toy Story'

# Check if the title exists in the dataset
if user_title in indices:
    # Get the index of the user-selected movie
    index = indices[user_title]

    # Calculate cosine similarity of the user-selected movie with all other movies
    cosine_similarities = cosine_similarity(x[index], x).flatten()

    # Get indices of the top 10 most similar movies, excluding the selected movie itself
    similar_indices = cosine_similarities.argsort()[-11:-1][::-1]

    # Display the titles of the top 10 similar movies
    recommended_movies = data['title'].iloc[similar_indices]
    print("Top 10 movies similar to '{}':".format(user_title))
    print(recommended_movies)
else:
    print("Movie not found in the dataset.")
