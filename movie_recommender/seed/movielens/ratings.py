import pandas as pd

ratings = pd.read_csv('ratings_small.csv')
movies = pd.read_csv('movies_metadata.csv.small')
names = pd.read_csv('names_small.csv.small')

x = pd.merge(names, ratings, how='inner', left_on='id',
        right_on='userId')
y = pd.merge(x, movies, how='inner', left_on='movieId',
        right_on='id')


ratings_small = y[ratings.columns.values]
ratings_small.to_csv('ratings_small.csv.small', index=False)
