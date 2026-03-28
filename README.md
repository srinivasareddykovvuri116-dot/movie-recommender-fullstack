# 🎬 Movie Recommendation System (Full Stack + ML)

## 🚀 Overview
A full-stack movie recommendation system that suggests personalized movies using machine learning techniques like collaborative filtering and cosine similarity.

## 🧠 Features
- Personalized movie recommendations based on user behavior
- Collaborative filtering using cosine similarity
- FastAPI backend for real-time recommendations
- Netflix-style responsive UI built with React
- Integration with external movie APIs for:
  - Posters
  - Ratings
  - Genres
  - Plot descriptions
- Dynamic search functionality
- Optimized performance using asynchronous API calls

## 🛠 Tech Stack
- **Frontend:** React.js, Axios
- **Backend:** FastAPI
- **Machine Learning:** Pandas, Scikit-learn
- **Others:** REST APIs

## 📂 Project Structure
movie-recommendation-system/
│
├── backend/
│ ├── main.py
│ ├── model.py
│ ├── requirements.txt
│
├── frontend/
│ ├── src/
│ ├── package.json
│
├── README.md
└── .gitignore


## ⚙️ Installation & Setup

### 🔹 Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

cd frontend
npm install
npm start

API Endpoints
GET /recommend?movie_name=... → Get recommended movies
GET /movies → Fetch all movies

Future Improvements
Add user authentication
Improve recommendation accuracy
Deploy using cloud platforms

👨‍💻 Author
K R S Srinivasa Reddy

