#python 3
import math, os, re, sys
import matplotlib.pyplot as plt
import multiprocessing
from joblib import Parallel, delayed
import json
import time

def get_count (dirname, fname, searchword):
    f = open(dirname + '/' + fname, "r")
    doc = f.read().lower()
    words = doc.split(" ")
    return words.count(searchword), len(words)

def frequency (searchword, num_cores):
    searchword =searchword.lower()
    freqs = [] 
    dirnames = []
    total_words = 0

    for dirname, subdirlist, filelist in os.walk("../WoR/"):
        dirnames.append(dirname)

    dirnames =dirnames[1:]

    for dirname in dirnames:
        print (dirname)
        freq = 0 
        filelist = os.listdir(dirname)
        print (len(filelist))
        occurances = Parallel(n_jobs=num_cores)(delayed(get_count)(dirname, fname, searchword) for fname in filelist)
        for j,k in occurances: 
            total_words = total_words + k 
            freq = freq + j
        freqs.append(freq)
    
    
    return freqs

result = frequency("slavery", 30)
for r in result:
    print (r)
