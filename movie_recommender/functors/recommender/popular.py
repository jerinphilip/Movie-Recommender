import booking_system.models as M
from django_pandas.io import read_frame

class PopularRecommender:

    def top(self, count):
        ratings = M.AggregateRating.objects.all()
        ratings = read_frame(ratings)
        quantile = 0.95
        return self.compute(ratings, count, quantile)

    def query_set(self, qualified):
        result = []
        for i, ql in qualified.iterrows():
            movie = M.Movie.objects.get(id=ql["movie"])
            result.append(movie)
        return result


    def top_by_genre(self, genre, count):
        genre = M.Genre.objects.get(genre=genre)
        ratings = M.AggregateRating.objects.filter(movie__genres__in=[genre])
        ratings = read_frame(ratings)
        quantile = 0.85
        return self.compute(ratings, count, quantile)

        
    def compute(self, ratings, count, quantile):
        C = ratings["average"].mean()
        m = ratings["count"].quantile(quantile)

        qualified = ratings

        def weighted_rating(x):
            v = x['count']
            R = x['average']
            return (v/(v+m) * R) + (m/(m+v) * C)

        qualified['wr'] = qualified.apply(weighted_rating, axis=1)
        qualified = qualified.sort_values('wr', ascending=False)
        qualified = qualified.head(count)
        return self.query_set(qualified)


