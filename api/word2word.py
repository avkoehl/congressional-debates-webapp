#python 3
import os, time, gensim, sys, json
from gensim.models import translation_matrix
from gensim.models import KeyedVectors
import matplotlib.pyplot as plt
from scipy import spatial
import numpy as np
import multiprocessing
from joblib import Parallel, delayed

def get_distances (fname, word, word2):
    sid = fname.split('/')[-1].split('.')[0]
    date = get_date(sid)
    print ("processing model: ", sid, date)
    model = gensim.models.Word2Vec.load(fname)

    sim = model.wv.similarity(word, word2)
    return date, sim 

def get_date (sessionid):
    datefile = "./data/congressional-debates/dates.csv"
    with open(datefile, "r") as f:
        for line in f:
            if line[0] != '#':
                tokens = line.rstrip().split(',')
                if tokens[0] == sessionid:
                    date = tokens[1]
                    return date

def make_json (distances):
    session = {}
    sessions = []
    for j,k in distances: 
      session['date'] = j 
      session['distance'] = k 
      sessions.append(session.copy())
    return json.dumps(sessions)

def get_filelist(word, word2):
  f = open("./data/embeddings/vocab/all.vocab","r")
  sessions = []
  contain_word = []

  for line in f:
    sessions.append(json.loads(line))

  for i in range (0, len(sessions)):
    session = sessions[i]
    if word in session["vocabulary"] and word2 in session["vocabulary"]:
      contain_word.append("./data/embeddings/models/"+session["id"]+".model")

  return contain_word


word = sys.argv[1].lower()
word2 = sys.argv[2].lower()
num_cores = int(sys.argv[3])


filelist = get_filelist(word, word2)
print (filelist)


f = open ("./outputs/2dist" + word + word2 + ".txt", "w")
distances = Parallel(n_jobs=num_cores)(delayed(get_distances)(fname, word, word2) for fname in filelist)
json = make_json(distances)
print (json, file=f)
print (json)


