#api for embeddings using flask
from flask import Flask, request, jsonify
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

print("load models")
model = SentenceTransformer('all-MiniLM-L6-v2') #make model
embeddings = np.load("movie_embeddings.npy") #load mebeddings using numpy
df = joblib.load("movie_metadata.pkl") #load movie metadata using pandas

#first api request POST, send user input

@app.route('/')
def home():
    return "Hello! This is the home page."

@app.route('/recommend', methods = ["POST"])
def recommend():
    data = request.get_json() #convert request to json
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query is required"}), 400

    #encode query using model
    query_embedding = model.encode(query)

    #now use cosine similarity to get closest movies
    
    scores = util.cos_sim(query_embedding, embeddings)[0] #[0] to remove the query number so only have tensor scores 
    
    #check if doesnt exist
    if scores is None or scores.numel() == 0:
        return jsonify({"error": "No scores"}), 400
    
    #covert scores from tensor to a numpy array
    scores_np = scores.cpu().numpy()
   
    #get top 5 movies or if less than 5 get len of array
    top_k = min(5, scores_np.shape[0])
    if top_k == 0:
        return jsonify({"error": "No scores found"}), 400
    
    #top movies is just indexes 
    #get top_k last elements
    #argsort just gets indexes
    top_movies = np.argsort(scores_np)[-top_k:]
    print(top_movies)
    results = []

    #use iloc to get indexes
    for idx in top_movies:
        results.append({
            "title": df.iloc[idx]['title'],
            "genres": df.iloc[idx]['parsed_genres'],  
            "overview": df.iloc[idx]['overview'],
            "score": round(float(scores[idx]), 4)  
        })
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
