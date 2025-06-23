import numpy as np
import plotly.express as px
import joblib

# Load your data
embeddings = np.load("movie_embeddings.npy")
df = joblib.load("movie_metadata.pkl")

# Simple manual PCA using numpy
#PCA simplifies the 384 dimensions from the embeddings
# Center the data so average is at zero
centered = embeddings - embeddings.mean(axis=0)

#Need covariance here to find out how do different features relate to eachother
cov_matrix = np.cov(centered.T)
#Need eigenvals and vecs to determine the 2 most meaningful dimensions
#Most meaningful means most variation in moviues
eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)

# Take top 2 components to get most meaningful differences between movies
top2_components = eigenvecs[:, -2:]

#project to a 2D graph
coords = centered @ top2_components

# Plot
fig = px.scatter(x=coords[:, 0], y=coords[:, 1], 
                hover_name=df['title'],
                title='Movie Embeddings')
fig.write_html("movie_plot.html")
