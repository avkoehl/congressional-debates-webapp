#python 3
import os, time, gensim, re, enchant
import multiprocessing
from joblib import Parallel, delayed
import json

""" Generate the word2vec models for each time slot using gensim skip grams model
        For each time slot,
            [1] use gensim to computer the word2vec model (skip grams sg=1)
"""


def get_clean_sentences(dirname, fname):
    d = enchant.Dict("en_US")
    stoplist = "mr on cay clay for a of the and to in".split()
    words = []
    with open(dirname + '/' + fname, "r") as ifile:
        lines = []
        for line in ifile:
            tokens = line.rstrip().split(" ")
            for t in tokens:
              t = re.sub("[^a-zA-Z]+", "", t).lower()
              if len(t) < 2:
                  continue
              if stoplist.count(t) == 0 and d.check(t):
                  words.append(t)
                

    c = 0
    ngram = []
    ngrams = []
    for w in words:
        if c < 10:
            ngram.append(w)
            c = c + 1
        else:
            ngrams.append(ngram)
            ngram = []
            c = 0
    
    return ngrams

def gen_models(dirname, i):
    print ("processing :", dirname)
    start = time.time()
    num_cores = multiprocessing.cpu_count()

    sentences = get_clean_sentences(dirname, "all.txt") 
    end = time.time()
    print ("parse sentence time: ", end - start)

    start1 = time.time()
    if sentences:
        model = gensim.models.Word2Vec(sentences, sg=1, window=5, workers=30)
        sessionid = str(i) + "_" + dirname.split('/')[-1]
        print (sessionid)
        model.save("./models/" + sessionid + ".model")
        modeldict = {}
        vocab = []
        for word in model.wv.vocab:
           vocab.append(word)
        modeldict["vocabulary"] = vocab
        modeldict["id"] = sessionid
        f = open("./vocab/" + sessionid + ".vocab", "w")
        Json = json.dumps(modeldict)
        print (Json, file=f)
        end2 = time.time()
        print ("time elapsed: ", end2 - start1)

    else:
        print ("empty!")

    return



def main ():
    path = "../congressional-globe/"
    num_cores = 10

    for i in range (23, 42):
        dirnames = []
        for dirname, subdirlist, filelist in os.walk(path + str(i)):
            if "session" in dirname:
                dirnames.append(dirname)

        Parallel(n_jobs=num_cores)(delayed(gen_models)(d, i) for d in dirnames)


if __name__ == "__main__":
    main()
