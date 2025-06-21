from fastapi import FastAPI, Request
from pydantic import BaseModel #like requests from flask
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

#convert the JSON query to a string
class QueryRequest(BaseModel):
    query: str

print("load models")
model = SentenceTransformer('all-MiniLM-L6-v2') #make model
embeddings = np.load("movie_embeddings.npy") #load mebeddings using numpy
df = joblib.load("movie_metadata.pkl") #load movie metadata using pandas

#first api request POST, send user input

@app.get("/")
def home():
    return {"message": "Hello! This is the home page."}

@app.post("/recommend")
def recommend(request: QueryRequest): #request is the query
    query = request.query.strip()

    if not query:
        return ({"error": "Query is required"}), 400

    #encode query using model
    query_embedding = model.encode(query)

    #now use cosine similarity to get closest movies
    
    scores = util.cos_sim(query_embedding, embeddings)[0] #[0] to remove the query number so only have tensor scores 
    
    #check if doesnt exist
    if scores is None or scores.numel() == 0:
        return ({"error": "No scores"}), 400
    
    #covert scores from tensor to a numpy array
    scores_np = scores.cpu().numpy()

    #get top 20 movies first
    top_n = 20
    
    #top movies is just indexes 
    #get top_n last elements
    #argsort just gets indexes
    top_movies = np.argsort(scores_np)[-top_n:]
    
    candidates = []
    #use iloc to get indexes
    for idx in top_movies:
        candidates.append({
            "title": df.iloc[idx]['original_title'],
            "genres": df.iloc[idx]['genres'],  
            "overview": df.iloc[idx]['overview'],
            "release date": df.iloc[idx]['release_date'],
            "popularity": df.iloc[idx]['popularity'],
            "vote_average": df.iloc[idx]['vote_average'],
            "poster_path": df.iloc[idx]['poster_path'],
            "score": round(float(scores[idx]), 4)  
        })
    #now sort by popularity to filter out the bad movies and get top 5 results
    candidates.sort(key=lambda i: i["popularity"], reverse=True)
    top_k = 5
    results = candidates[:top_k]
    
    return results

#to run do uvicorn app:app --reload , dont use reload if testing test cases