from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import requests
import os
from dotenv import load_dotenv

# 🔐 Load env
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

app = FastAPI()

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Globals
similarity = None
movies_list = None

# 🚀 Load model safely
def load_model():
    global similarity, movies_list

    if not os.path.exists("model/similarity.pkl"):
        print("⚡ Model not found. Building now... - main.py:32")
        import model  # runs model.py

    print("✅ Loading model... - main.py:35")
    similarity = pickle.load(open("model/similarity.pkl", "rb"))
    movies_list = pickle.load(open("model/movies.pkl", "rb"))

# 🔥 Call once
load_model()

# -------------------- ROUTES --------------------

@app.get("/")
def home():
    return {"message": "Movie Recommender API Running 🚀"}


@app.get("/movies")
def get_movies():
    return {"movies": movies_list}


@app.get("/recommend/{movie}")
def recommend(movie: str):
    if movie not in movies_list:
        return {"recommendations": []}

    try:
        idx = movies_list.index(movie)

        # Get similarity scores
        sim_scores = list(enumerate(similarity[idx]))

        # Sort movies based on similarity
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

        movie_indices = [i[0] for i in sim_scores]

        return {"recommendations": [movies_list[i] for i in movie_indices]}

    except Exception:
        return {"recommendations": []}


# 🔥 Secure OMDb API route
@app.get("/movie-details/{movie}")
def get_movie_details(movie: str):
    try:
        url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie}"
        res = requests.get(url).json()

        return {
            "poster": res.get("Poster"),
            "rating": res.get("imdbRating"),
            "year": res.get("Year"),
            "genre": res.get("Genre"),
            "plot": res.get("Plot")
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching movie details")