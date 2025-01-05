import json
import os
import random

import nltk
nltk.download('wordnet')

from nltk.corpus import wordnet

def calc_scr(wrd):
    SCRS = {
        'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
        'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3,
        'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
        'y': 4, 'z': 10
    }

    return sum(SCRS.get(char, 0) for char in wrd.lower()) + len(wrd)

def chk(ans, wrd):
    return ans.strip().lower() == wrd.lower()

def get_rndm(optn_map, optn):
    wrds = optn_map.get(optn, [])

    if not wrds:
        return None
    
    random.shuffle(wrds)
    for wrd in wrds:
        synsets = wordnet.synsets(wrd)
        if synsets:
            defn = synsets[0].definition()
            scr = calc_scr(wrd)
            return wrd, defn, scr

def scramble(wrd):
    return ''.join(random.sample(wrd, len(wrd)))

def set_wrds():
    cache_file = "word_cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)

    optn_map = {'easy': [], 'standard': [], 'hard': [], 'expert': []}
    wrds = [w for w in wordnet.words() if len(w) > 4]

    for wrd in wrds:
        if wrd.isalpha():
            scr = calc_scr(wrd)
            if scr <= 20:
                optn_map['easy'].append(wrd)
            elif 20 < scr <= 25:
                optn_map['standard'].append(wrd)
            elif 25 < scr <= 30:
                optn_map['hard'].append(wrd)
            else:
                optn_map['expert'].append(wrd)

    with open(cache_file, "w") as f:
        json.dump(optn_map, f)

    return optn_map

