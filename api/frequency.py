#!/usr/bin/python3
# -*- coding: utf-8 -*-


##
# input parameters:
#       argv[1] = word
#       argv[2] = num_cores
#       argv[3] = corpus
#
# several helper functions and main for each corpus
# functions with cg_ in front are congression globe
#                wor_ is for war of rebellion
##

# dependencies
import math, os, re, sys, json, time
import multiprocessing
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

# paths
def get_paths(corpus):
    dfilepath = './data/' + corpus + '/dates.csv'
    corpuspath =  './data/' + corpus + '/'

# given directory get the number of words and number of occurances
def get_count (dirname, fname, searchword):
    f = open(dirname + '/' + fname, "r")
    doc = f.read().lower()
    words = doc.split(" ")
    return words.count(searchword), len(words)

# given session id return the date 
def cg_get_date (sessionid):
    datefile = './data/congressional-globe/dates.csv'
    with open(datefile, "r") as f:
        for line in f:
            if line[0] != '#':
                tokens = line.rstrip().split(',')
                if tokens[0] == sessionid:
                    date = tokens[1]
                    return date

def cg_calc_frequency (searchword, dirname):

    date = cg_get_date(dirname.split('/')[-2] + "_" + dirname.split('/')[-1])
    print ("Processing session: ", dirname.split('/')[-2] + "_" + dirname.split('/')[-1])
    total_occurances = 0
    total_words = 0
    frequency = 0
    occurances = []

    total_occurances, total_words = get_count(dirname, "all.txt", searchword)

    if (total_occurances != 0 and total_words != 0):
       frequency = float(total_occurances) / total_words
    else:
       frequency = 0  

    if (frequency > 0):
       return date, math.log10(frequency)
    else:
       return date, 0

def cg_frequency (searchword, num_cores):
    searchword =searchword.lower()
    path = './data/congressional-globe/'
    freqs = [] 
    dates = []
    sessions = []
    dirnames = []
    for i in range (23, 43): #for each Congress
        for dirname, subdirlist, filelist in os.walk(path + str(i)):
            dirnames.append(dirname)

    dirnames.sort()
    directories = []

    for dirname in dirnames:
       if "session" in dirname and os.listdir(dirname):
          directories.append(dirname)

    sessions = (Parallel(n_jobs=num_cores)(delayed(cg_calc_frequency)(searchword, d) for d in directories))

    session = {}
    session_list = [] 
    for i in range (0, len(sessions)):
        session['date'] = sessions[i][0] 
        session['frequency'] = sessions[i][1]
        session_list.append(session.copy())
    return session_list


word = sys.argv[1]



def main():
    word = sys.argv[1]
    cores = sys.argv[2]
    f = open ("./outputs/" + word + ".txt", "w")

    start = time.time()
    result = cg_frequency(word, int(cores))
    end = time.time()

    res_json = json.dumps(result)

    print (res_json, file=f)
    print (res_json)
    print ("time elapsed:", end - start)


if __name__ == "__main__":
    main()
