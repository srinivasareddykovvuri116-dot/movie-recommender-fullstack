from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import requests
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 🔥 STEP 1: Build model if not exists
if not os.path.exists("model/similarity.pkl"):
    print("⚡ Model not found. Building now... - main.py:28")
    import model   # this runs model.py

# 🔥 STEP 2: Load model AFTER build
similarity_df = pickle.load(open("model/similarity.pkl", "rb"))
movies_list = pickle.load(open("model/movies.pkl", "rb"))



# -------------------- ROUTES --------------------

@app.get("/")
def home():
    return {"message": "Movie Recommender API Running 🚀"}


@app.get("/movies")
def get_movies():
    return {"movies": movies_list}


@app.get("/recommend/{movie}")
def recommend(movie: str):
    if movie not in similarity_df.index:
        return {"recommendations": []}

    similar = similarity_df[movie].sort_values(ascending=False)[1:6]
    return {"recommendations": list(similar.index)}


# 🔥 NEW: Secure OMDb API route
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