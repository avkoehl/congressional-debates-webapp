#python 3
import math, os, re
import matplotlib.pyplot as plt
import multiprocessing
from joblib import Parallel, delayed

def get_dates ():
    dates = []
    datefile = "/var/www/html/congress/text/dates.csv"
    with open(datefile, "r") as f:
        for line in f:
            if line[0] != '#':
                tokens = line.rstrip().split(',')
                dates.append(tokens[1])
    return dates 

def get_count (dirname, fname, searchword):
    f = open(dirname + '/' + fname, "r")
    doc = f.read()
    words = doc.split(" ")
    return words.count(searchword)

def get_wordcount (dirname, fname):
    f = open(dirname + '/' + fname, "r")
    doc = f.read()
    words = doc.split(" ")
    return len(words)


def frequency (searchword):
    dates = get_dates()
    path = '/var/www/html/congress/text/'
    freqs = [] 
    for i in range (23, 43): #for each Congress
        print ("Processing Congress Number: ", i)
        #get the sessions
        dirnames = []
        for dirname, subdirlist, filelist in os.walk(path + str(i)):
            dirnames.append(dirname)


        for dirname in dirnames:
            if "session" in dirname:

                total_occurances = 0
                total_words = 0
               
                filelist = os.listdir(dirname)
                num_cores = multiprocessing.cpu_count()

                ### get list of word counts each entry is different file
                occurances = Parallel(n_jobs=num_cores)(delayed(get_count)(dirname, fname, searchword) for fname in filelist)

                ### get list of total word counts for each file
                wc = Parallel(n_jobs=num_cores)(delayed(get_wordcount)(dirname, fname) for fname in filelist)

                for i in range(0, len(occurances)):
                    total_occurances = total_occurances + occurances[i]
                    total_words = total_words + wc[i]

                #
                #for fname in filelist:
                #    total_occurances = total_occurances + get_count(dirname, fname, searchword)
                #    total_words = total_words + get_wordcount (dirname, fname) 

                ## if session dir is empty or the word never occured!
                if (total_occurances != 0 and total_words != 0):
                    frequency = float(total_occurances) / total_words
                else:
                    frequency = 0  

                if (frequency > 0):
                    freqs.append(math.log10(frequency))
                else:
                    freqs.append(0)

    session = {}
    sessions = [] 
    for i in range (0, len(freqs)):
        session['date'] = dates[i] 
        session['frequency'] = freqs[i]
        sessions.append(session.copy())
    return sessions

