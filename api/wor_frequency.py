#python 3
import math, os, re, sys
import matplotlib.pyplot as plt
import multiprocessing
from joblib import Parallel, delayed
import json
import time

def get_count (d, fname, searchword):
    f = open(d + '/' + fname, "r")
    doc = f.read().lower()
    words = doc.split(" ")
    return words.count(searchword), len(words)

def frequency (searchword, d):

    total_words = 0
    freq = 0 

    filelist = os.listdir(d)
    for fname in filelist:
        res = get_count(d, fname, searchword)

        freq = freq + res[0]
        total_words = total_words + res[1]

    return freq, total_words


def main(searchword, num_cores):
    searchword =searchword.lower()
    dirnames = []
    freqs = [] 
    wc = []

    for dirname, subdirlist, filelist in os.walk("./data/war-of-rebellion"):
        dirnames.append(dirname)
    dirnames = dirnames[1:] # to get rid of self (root)  in directory list

    result = Parallel(n_jobs=num_cores)(delayed(frequency)(searchword, d) for d in dirnames)
    for f,o in result:
        freqs.append(f)
        wc.append(o)

    return freqs, wc


if __name__ == "__main__":
    freq, wc = main("contraband", 20)
    for i in range(0, len(freq)):
      print ("serial #: ", '%04d' % int(i), " ", '%04d' % int(freq[i]), " || ",  (freq[i] / wc[i]))
