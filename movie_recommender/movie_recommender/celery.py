from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_recommender.settings')

app = Celery('movie_recommender',
             broker='redis://localhost:6379/0',
             include=['functors.booker'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
