from haystack import indexes
from .models import Movie,Genre,Theater,CrewProfile

class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    id = indexes.EdgeNgramField(model_attr='id')
    synopsis = indexes.EdgeNgramField(model_attr='synopsis')
    # language = indexes.EdgeNgramField(model_attr='language')
    # crew = indexes.EdgeNgramField(model_attr='crew')
    # genres = indexes.EdgeNgramField(model_attr='genres')
    def get_model(self):
      return Movie

class GenreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='genre')
    id = indexes.EdgeNgramField(model_attr='id')

    def get_model(self):
        return Genre


class TheaterIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='name')
    id = indexes.EdgeNgramField(model_attr='id')

    def get_model(self):
        return Theater

class CrewProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='name')
    id = indexes.EdgeNgramField(model_attr='id')

    def get_model(self):
        return CrewProfile
