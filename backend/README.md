
# Setting up


### Virtual Environment
Install `virtualenv` from os repos.

```
virtualenv env --python=/usr/bin/python3
. env/bin/activate
```

### Install requirements

```
pip install -r requirements.txt
```

### Django setup

```
python manage.py makemigrations
python manage.py migrate
```


