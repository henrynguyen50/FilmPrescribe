import pandas as pd

df = pd.read_csv("TMDB_movie_dataset.csv")

filtered_df = df[df["vote_count"] >= 100]
filtered_df.to_csv("TMDBMovieData", index=False)