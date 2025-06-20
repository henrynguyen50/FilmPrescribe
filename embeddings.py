import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import joblib
import ast
import plotly.express as px

df = pd.read_csv("topmovies.csv")

#only grab relevant columns
df_subset = df[["title", "genres", "keywords", "overview", "release_date"]]
#fill in missing cols
df_subset = df_subset.fillna("")

df_subset["metadata"] = df_subset["title"] + " " + df_subset["overview"] + " " + df_subset["genres"] + " " + df_subset["keywords"]
#load embedding model
print(df_subset["metadata"].head())

model = SentenceTransformer('all-MiniLM-L6-v2')


print("Making embeddings")
embeddings = model.encode(df_subset['metadata'].tolist(), show_progress_bar = True)

#save embeddings then dataframe 
np.save("movie_embeddings.npy", embeddings)
joblib.dump(df_subset, "movie_metadata.pkl")

print("Embeddings saved")
