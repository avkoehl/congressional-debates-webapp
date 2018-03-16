#python 3
import os, time, gensim
import multiprocessing
from joblib import Parallel, delayed

""" Generate the word2vec models for each time slot using gensim skip grams model
        For each time slot,
            [1] use gensim to computer the word2vec model (skip grams sg=1)
"""

##

def get_sentences(dirname, fname):
    myfile = open(dirname + '/' + fname, "r")
    lines =  myfile.readlines()
    return lines

def gen_models(dirname, all_sentences, i):
    model = gensim.models.Word2Vec(all_sentences, sg=1, window=5, workers=8)
    sessionid = str(i) + "_" + dirname.split('/')[-1]
    print (model.wv["slave"])
    model.save(sessionid + ".model")

    return

def models ():
    path = "/var/www/html/congress/text/"

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
                end = time.time()
                start1 = time.time()
                print ("parse sentence time: ", end - start)


                for k in range(len(sentences)):
                    for j in range(len(sentences[k])):
                        all_sentences.append(sentences[k][j].split())


                if all_sentences:
                    gen_models(dirname, all_sentences, i)
                    end2 = time.time()
                    print ("time elapsed: ", end2 - start1)
                else:
                    print ("empty!")


models()
