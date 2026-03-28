import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [movies, setMovies] = useState([]);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [posters, setPosters] = useState([]);
  const [details, setDetails] = useState([]);

  // Load movies
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/movies")
      .then(res => setMovies(res.data.movies))
      .catch(err => console.log(err));
  }, []);

  // 🔥 Clean movie name
  const cleanTitle = (movieName) => {
    return movieName
      .replace(/\(\d{4}\)/, "")
      .replace(/[^a-zA-Z0-9 ]/g, "")
      .trim();
  };

  // 🔥 Fetch poster
  const fetchPoster = async (movieName) => {
    try {
      const res = await axios.get(
        `https://www.omdbapi.com/?apikey=a1ccc36a&t=${encodeURIComponent(cleanTitle(movieName))}`
      );

      return res.data?.Poster && res.data.Poster !== "N/A"
        ? res.data.Poster
        : null;
    } catch {
      return null;
    }
  };

  // 🔥 Fetch full details (UPDATED)
  const fetchDetails = async (movieName) => {
    try {
      const res = await axios.get(
        `https://www.omdbapi.com/?apikey=a1ccc36a&t=${encodeURIComponent(cleanTitle(movieName))}`
      );

      return {
        rating: res.data?.imdbRating || "N/A",
        year: res.data?.Year || "N/A",
        genre: res.data?.Genre || "N/A",
        plot: res.data?.Plot || "No description available"
      };
    } catch {
      return {
        rating: "N/A",
        year: "N/A",
        genre: "N/A",
        plot: "No description available"
      };
    }
  };

  // 🔥 Get recommendations
  const getRecommendations = async () => {
    if (!selected) return;

    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/recommend/${encodeURIComponent(selected)}`
      );

      const moviesList = res.data.recommendations;
      setRecommendations(moviesList);

      // Posters
      const posterList = await Promise.all(
        moviesList.map(movie => fetchPoster(movie))
      );
      setPosters(posterList);

      // Details
      const detailsList = await Promise.all(
        moviesList.map(movie => fetchDetails(movie))
      );
      setDetails(detailsList);

    } catch (err) {
      console.log(err);
    }
  };

  // Filter search
  const filteredMovies = movies.filter(movie =>
    movie.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="app">
      <h1>🎬 Movie Recommender</h1>

      <input
        type="text"
        placeholder="Search movie..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="movie-list">
        {filteredMovies.slice(0, 10).map((movie, index) => (
          <div
            key={index}
            className="movie-item"
            onClick={() => setSelected(movie)}
          >
            {movie}
          </div>
        ))}
      </div>

      <button onClick={getRecommendations}>Recommend</button>

      <h2>Recommendations</h2>

      <div className="grid">
        {recommendations.map((movie, index) => (
          <div className="card" key={index}>
            <img
              src={
                posters[index] ||
                "https://via.placeholder.com/300x450?text=No+Image"
              }
              alt={movie}
            />

            <p className="title">{movie}</p>

            <div className="info">
              <span>⭐ {details[index]?.rating}</span>
              <span>📅 {details[index]?.year}</span>
            </div>

            {/* 🔥 NEW FEATURES */}
            <p className="genre">🎭 {details[index]?.genre}</p>

            <p className="plot">
              {details[index]?.plot?.slice(0, 100)}...
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;