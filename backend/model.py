import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

movies_path = os.path.join(BASE_DIR, "data", "movies.csv")
ratings_path = os.path.join(BASE_DIR, "data", "ratings.csv")

movies = pd.read_csv("../data/movies.csv")
ratings = pd.read_csv("../data/ratings.csv")
# Merge
data = pd.merge(ratings, movies, on="movieId")

# Matrix
movie_matrix = data.pivot_table(
    index='title',
    columns='userId',
    values='rating'
).fillna(0)

# Similarity
similarity = cosine_similarity(movie_matrix)

similarity_df = pd.DataFrame(
    similarity,
    index=movie_matrix.index,
    columns=movie_matrix.index
)

# Save
os.makedirs("model", exist_ok=True)

pickle.dump(similarity_df, open("model/similarity.pkl", "wb"))
pickle.dump(movie_matrix.index.tolist(), open("model/movies.pkl", "wb"))

print("✅ Model built successfully! - model.py:40")