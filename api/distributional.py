#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, time, gensim, sys, json
from gensim.models import translation_matrix
from gensim.models import KeyedVectors
import matplotlib.pyplot as plt
from scipy import spatial
import numpy as np
import multiprocessing
from joblib import Parallel, delayed

""" Distributional model for Linguistic shift time sereis construction
        For each time slot,
            [1] load in gensime word2vec models generated wiht gensim_models.py 
            [2] align all vectors to the last vector
            [3] compute the distances between each vector and the first vector (just model["searchword"] vectors)
            [3] plot a time series of the distances between vectors
"""


def smart_procrustes_align_gensim(base_embed, other_embed, words=None):
    """ Procrustes align two gensim word2vec models (to allow for comparison between same word across models).
    Code ported from HistWords <https://github.com/williamleif/histwords> by William Hamilton <wleif@stanford.edu>.
            (With help from William. Thank you!)
    First, intersect the vocabularies (see `intersection_align_gensim` documentation).
    Then do the alignment on the other_embed model.
    Replace the other_embed model's syn0 and syn0norm numpy matrices with the aligned version.
    Return other_embed.
    If `words` is set, intersect the two models' vocabulary with the vocabulary in words (see `intersection_align_gensim` documentation).
    """
    # make sure vocabulary and indices are aligned
    in_base_embed, in_other_embed = intersection_align_gensim(base_embed, other_embed, words=words)

    # get the embedding matrices
    base_vecs = in_base_embed.wv.syn0norm
    other_vecs = in_other_embed.wv.syn0norm

    # just a matrix dot product with numpy
    m = other_vecs.T.dot(base_vecs)
    # SVD method from numpy
    u, _, v = np.linalg.svd(m)
    # another matrix operation
    ortho = u.dot(v)
    # Replace original array with modified one
    # i.e. multiplying the embedding matrix (syn0norm)by "ortho"
    other_embed.wv.syn0norm = other_embed.wv.syn0 = (other_embed.wv.syn0norm).dot(ortho)
    return other_embed


def intersection_align_gensim(m1,m2, words=None):
    """
    Intersect two gensim word2vec models, m1 and m2.
    Only the shared vocabulary between them is kept.
    If 'words' is set (as list or set), then the vocabulary is intersected with this list as well.
    Indices are re-organized from 0..N in order of descending frequency (=sum of counts from both m1 and m2).
    These indices correspond to the new syn0 and syn0norm objects in both gensim models:
        -- so that Row 0 of m1.syn0 will be for the same word as Row 0 of m2.syn0
        -- you can find the index of any word on the .index2word list: model.index2word.index(word) => 2
    The .vocab dictionary is also updated for each model, preserving the count but updating the index.
    """

    # Get the vocab for each model
    vocab_m1 = set(m1.wv.vocab.keys())
    vocab_m2 = set(m2.wv.vocab.keys())

    # Find the common vocabulary
    common_vocab = vocab_m1&vocab_m2
    if words: common_vocab&=set(words)

    # If no alignment necessary because vocab is identical...
    if not vocab_m1-common_vocab and not vocab_m2-common_vocab:
        return (m1,m2)

    # Otherwise sort by frequency (summed for both)
    common_vocab = list(common_vocab)
    common_vocab.sort(key=lambda w: m1.wv.vocab[w].count + m2.wv.vocab[w].count,reverse=True)

    # Then for each model...
    for m in [m1,m2]:
        # Replace old syn0norm array with new one (with common vocab)
        indices = [m.wv.vocab[w].index for w in common_vocab]
        old_arr = m.wv.syn0norm
        new_arr = np.array([old_arr[index] for index in indices])
        m.wv.syn0norm = m.wv.syn0 = new_arr

        # Replace old vocab dictionary with new one (with common vocab)
        # and old index2word with new one
        m.index2word = common_vocab
        old_vocab = m.wv.vocab
        new_vocab = {}
        for new_index,word in enumerate(common_vocab):
            old_vocab_obj=old_vocab[word]
            new_vocab[word] = gensim.models.word2vec.Vocab(index=new_index, count=old_vocab_obj.count)
        m.wv.vocab = new_vocab

    return (m1,m2)


def get_distances (base, fname, word):
    sid = fname.split('/')[-1].split('.')[0]
    date = get_date(sid)
    #print ("processing model: ", sid, date)
    bmodel = gensim.models.Word2Vec.load(base)
    model = gensim.models.Word2Vec.load(fname)
    bmodel.init_sims()
    model.init_sims()
    aligned = smart_procrustes_align_gensim (bmodel, model)

    base = bmodel.wv[word]
    current = aligned.wv[word]
    sim = 1 - spatial.distance.cosine(base, current)


    return date, sim 

def get_date (sessionid):
    datefile = './data/congressional-globe/dates.csv'
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
      session['similarity'] = k 
      sessions.append(session.copy())
    return json.dumps(sessions)

def get_filelist(word):
    f = open("./data/embeddings/vocab/all.vocab","r")
    sessions = []
    contain_word = []

    for line in f:
        sessions.append(json.loads(line))

    for i in range (0, len(sessions)):
        session = sessions[i]
        if word in session["vocabulary"]:
            contain_word.append("./data/embeddings/models/"+session["id"]+".model")

    return contain_word[0], contain_word


def main():
    word = sys.argv[1].lower()
    num_cores = int(sys.argv[2])

    base, filelist = get_filelist(word)

    distances = Parallel(n_jobs=num_cores)(delayed(get_distances)(base, fname, word) for fname in filelist)
    json = make_json(distances)
    print (json)


if __name__ == "__main__":
    main()

