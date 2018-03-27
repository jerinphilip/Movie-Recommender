
# Setting up


### Virtual Environment
Install `virtualenv` from os repos.

```
sudo apt-get install virtualenv
```

```
virtualenv env --python=/usr/bin/python3
. env/bin/activate
```

### Install requirements

```
pip install -r requirements.txt
```

### Django setup

Move to the `movie_recommender` folder.

```
python manage.py makemigrations
python manage.py migrate
```

Optional, setup superuser, to login to `/admin`.

```
python manage.py createsuperuser
```

### Seeding data

```bash
python manage.py seed --path seed/movie_metadata.csv
```

### Verifying (move to movie_recommender folder first)
```
python manage.py runserver
```
* Login to localhost:8000/admin (assuming you created admin/superuser above)



