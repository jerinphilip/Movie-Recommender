import booking_system.models as M
from django_pandas.io import read_frame
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import pandas as pd


class CBRecommender:
    def top(self, count):
        movies = M.Movie.objects.all()
        movies = read_frame(movies)
        #print(movies)

        movies['description'] = movies['tagline'] + movies['synopsis']
        tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(movies['description'])
        print(tfidf_matrix.shape)

        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        movies = movies.reset_index()
        titles = movies['title']
        indices = pd.Series(movies.index, index=movies['title'])

        def get_recommendations(title):
            idx = indices[title]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:count]
            movie_indices = [i[0] for i in sim_scores]
            return movie_indices

        sample = movies.ix[3]['title']
        recommendations = get_recommendations(sample)
        objs = []
        for recommendation in recommendations:
            idx = (movies.ix[recommendation]['id'])
            movie = M.Movie.objects.get(id=idx)
            objs.append(movie)
        return objs
        













    
