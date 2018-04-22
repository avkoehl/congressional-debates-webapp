#python 3
import os, time, gensim
import multiprocessing
from joblib import Parallel, delayed
import json

""" Generate the word2vec models for each time slot using gensim skip grams model
        For each time slot,
            [1] use gensim to computer the word2vec model (skip grams sg=1)
"""

##

def get_sentences(dirname, fname):
    myfile = open(dirname + '/' + fname, "r")
    lines = []
    for line in myfile:
      lines.append(line.lower())
    return lines

def gen_models(dirname, all_sentences, i):
    model = gensim.models.Word2Vec(all_sentences, sg=1, window=5, workers=30)
    sessionid = str(i) + "_" + dirname.split('/')[-1]
    print (sessionid)
    model.save("./wor_models/" + sessionid + ".model")
    modeldict = {}
    vocab = []
    for word in model.wv.vocab:
      vocab.append(word)
    modeldict["vocabulary"] = vocab
    modeldict["id"] = sessionid
    f = open("./vocab/all.vocab", "a")
    Json = json.dumps(modeldict)
    print (Json, file=f)
    return

def models ():
    path = "../text/"

    for i in range (23, 42):
        dirnames = []
        for dirname, subdirlist, filelist in os.walk(path + str(i)):
            dirnames.append(dirname)

        for dirname in dirnames:
            if "session" in dirname:
                all_sentences = []
                start = time.time()
                filelist = os.listdir(dirname)
                num_cores = multiprocessing.cpu_count()

                sentences = Parallel(n_jobs=num_cores)(delayed(get_sentences)(dirname, fname) for fname in filelist)


                for k in range(len(sentences)):
                    for j in range(len(sentences[k])):
                        all_sentences.append(sentences[k][j].split())

                end = time.time()
                print ("parse sentence time: ", end - start)


                start1 = time.time()
                if all_sentences:
                    gen_models(dirname, all_sentences, i)
                    end2 = time.time()
                    print ("time elapsed: ", end2 - start1)
                else:
                    print ("empty!")


models()
