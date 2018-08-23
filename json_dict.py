import json
import pickle

def dump_hist(hist):
    with open('history.json', 'wb') as f:
        pickle.dump(hist, f)

def load_hist():
    with open('history.json', 'rb') as f:
        data = pickle.load(f)
    return data

hist = {}
