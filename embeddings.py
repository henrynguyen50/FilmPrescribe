import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import joblib
import ast
import plotly.express as px

df = pd.read_csv("TMDBMovieData.csv")

#only grab relevant columns
df_subset = df[["original_title", "genres", "keywords", "tagline", "overview", "release_date","poster_path","vote_average","popularity"]]
#fill in missing cols
df_subset = df_subset.fillna("")

df_subset["metadata"] = df_subset["original_title"] + " " + df_subset["overview"] + " " + df_subset["genres"] + " " + df_subset["keywords"] + " " + df_subset["tagline"]
#load embedding model
print(df_subset["metadata"].head())

model = SentenceTransformer('all-MiniLM-L6-v2')


print("Making embeddings")
embeddings = model.encode(df_subset['metadata'].tolist(), show_progress_bar = True)

#save embeddings then dataframe 
np.save("movie_embeddings.npy", embeddings)
joblib.dump(df_subset, "movie_metadata.pkl")

print("Embeddings saved")
