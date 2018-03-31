import os
import pandas as pd
from ast import literal_eval
from pprint import pprint

files = [
    "credits.csv",
    "keywords.csv",
    "links.csv",
    "links_small.csv",
    "movies_metadata.csv",
    "ratings.csv",
    "ratings_small.csv",
]

def load(fdir):
    _export = {}
    for fname in files:
        key = fname.replace(".csv", "")
        fname = '{}.small'.format(fname)
        fpath = os.path.join(fdir, fname) 
        _export[key] = pd.read_csv(fpath)
    return _export



def cast(serialized):
    dt = literal_eval(serialized)
    pprint(dt)
    return dt

def director(crew):
    for member in crew:
        if member['job'] == 'Director':
            return member
    return None

