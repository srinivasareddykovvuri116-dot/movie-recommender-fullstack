import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# 📁 Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
movies_path = os.path.join(BASE_DIR, "data", "movies.csv")

# 📊 Load data
movies = pd.read_csv(movies_path)

# 🧹 Clean genres
movies['genres'] = movies['genres'].fillna('').str.replace('|', ' ', regex=False)

# ⚡ TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])

# ⚡ Compute similarity (efficient)
similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

# 🎯 Save
os.makedirs("model", exist_ok=True)

pickle.dump(similarity, open("model/similarity.pkl", "wb"))
pickle.dump(movies['title'].tolist(), open("model/movies.pkl", "wb"))

print("✅ Lightweight model built successfully! - model.py:30")