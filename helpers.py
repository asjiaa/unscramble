import json
import os
import random

import nltk
nltk.download('wordnet')

from nltk.corpus import wordnet

def calc_scr(wrd):
    """Calculate the 'difficulty score' of given word

    Args:
        wrd (str): Miscellaneous single word string

    Returns:
        scr (int): 'Difficulty score' of word calculated through structure and length     
    
    """

    # Dictionary associating each alphabetical letter to score based on commonality
    SCRS = {
        'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
        'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3,
        'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
        'y': 4, 'z': 10
    }

    # Calculate 'difficulty score' through sum of letter scores and word length
    return sum(SCRS.get(char, 0) for char in wrd.lower()) + len(wrd)

def chk(ans, wrd):
    """Check if two strings are alphabetically identical

    Args:
        ans (str): Miscellaneous single word string
        wrd (str): Miscellaneous single word string input

    Returns:
        bool: Depending on whether strings are identical. True for success. False otherwise.
    
    """
    return ans.strip().lower() == wrd.lower()

def get_rndm(optn_map, optn):
    """Get random word from dictionary, dependent on category

    Args:
        optn_map (dict): Dictionary categorizing words under four (4) difficulties
        optn (str): Corresponding to specific difficulty category

    Returns:
        wrd, defn, scr: The generated word. Corresponding definition. Corresponding difficulty score.
    
    """
    # Fetch list of words corresponding to difficulty option
    wrds = optn_map.get(optn, [])

    if not wrds:
        return None
    
    # Reorganize list of words
    random.shuffle(wrds)

    # Iterate through shuffled set of words
    for wrd in wrds:
        # Fetch synsets corresponding to word, allows retrieval of definitions (WordNet)
        synsets = wordnet.synsets(wrd)
        if synsets:
            defn = synsets[0].definition()
            scr = calc_scr(wrd)
            return wrd, defn, scr

def scramble(wrd):
    """Get random word from dictionary, dependent on category

    Args:
        wrd: Miscellaneous single word string

    Returns:
        str: Entered string with letters reorganized
    
    """
    return ''.join(random.sample(wrd, len(wrd)))

def set_wrds():
    """Create dictionary where values are lists of words, keys correspond with difficulty settings

    Returns:
        dict: Dictionary of words
    
    """

    cache_file = "word_cache.json"

    # Check existence of cache file
    if os.path.exists(cache_file):
        # Generate dict from the cache file, if exists
        with open(cache_file, "r") as f:
            return json.load(f)
        
    # Initialize dict to store words corresponding to difficulty levels
    optn_map = {'easy': [], 'standard': [], 'hard': [], 'expert': []}
    wrds = [w for w in wordnet.words() if len(w) > 4]

    # Categorize words dependent on difficulty scores
    for wrd in wrds:
        # Ensure only single word strings in dict
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
    
    # Write into cache file for more efficient access
    with open(cache_file, "w") as f:
        json.dump(optn_map, f)

    return optn_map

