import re
import enchant


def get_words (fname):
    d = enchant.Dict("en_US") 
    stoplist = "mr on cay clay for a of the and to in".split()
    
    words = []
    with open (fname, "r") as ifile:
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
