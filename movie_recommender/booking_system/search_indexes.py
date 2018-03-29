from haystack import indexes
from .models import Movie,Genre,Language
 
class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    synopsis = indexes.CharField(model_attr='synopsis')
    # language = indexes.CharField(model_attr='language')
    # crew = indexes.CharField(model_attr='crew')
    # genres = indexes.CharField(model_attr='genres')
  
    def get_model(self):
      return Movie

class GenreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    genre = indexes.CharField(model_attr='genre')
  
    def get_model(self):
        return Genre
