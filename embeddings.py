import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import joblib
import ast

df = pd.read_csv("movies.csv")

def parsed_genres(genre_str):
    try:
        genres = ast.literal_eval(genre_str) #convert csv to pyhton literal
        return " ".join([g['name'] for g in genres])
    except Exception:
        return ""
    
#make new col for the extracted genres
df['parsed_genres'] = df['genres'].apply(parsed_genres)

#now combine the titles, genres, and small overview of movies
df['metadata'] = df['title'].fillna('') + ". " + df['parsed_genres'].fillna('') + ". " + df['overview'].fillna('')

#load embedding model

model = SentenceTransformer('all-MiniLM-L6-v2')


print("Making embeddings")
embeddings = model.encode(df['metadata'].tolist(), show_progress_bar = True)

#save to disk
#save embeddings then dataframe 
np.save("movie_embeddings.npy", embeddings)
joblib.dump(df, "movie_metadata.pkl")

print("Embeddings saved")