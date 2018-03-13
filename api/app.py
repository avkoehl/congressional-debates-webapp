from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import math, os, re, json
import matplotlib.pyplot as plt
import multiprocessing
from joblib import Parallel, delayed

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Linguistic Historic Word Change API"

@app.route('/frequency', methods=['GET'])
def get_frequency():
    word = request.args.get('word', type = str)
    num_cores = multiprocessing.cpu_count()
    freq_array = frequency(word, num_cores)
    response = jsonify(freq_array)
    return response;


def get_date (sessionid):
    datefile = "../text/dates.csv"
    with open(datefile, "r") as f:
        for line in f:
            if line[0] != '#':
                tokens = line.rstrip().split(',')
                if tokens[0] == sessionid:
                    date = tokens[1]
                    return date


def get_count (dirname, fname, searchword):
    f = open(dirname + '/' + fname, "r")
    doc = f.read()
    words = doc.split(" ")
    return words.count(searchword), len(words)

def frequency (searchword, num_cores):
    path = '../text/'
    freqs = [] 
    dates = []
    for i in range (23, 43): #for each Congress
        print ("Processing Congress Number: ", i)
        #get the sessions
        dirnames = []
        for dirname, subdirlist, filelist in os.walk(path + str(i)):
            dirnames.append(dirname)


        dirnames.sort()
        for dirname in dirnames:
            if "session" in dirname and os.listdir(dirname):
                date = get_date(str(i) + "_" + dirname.split('/')[-1])
                total_occurances = 0
                total_words = 0
                filelist = os.listdir(dirname)
                occurances = Parallel(n_jobs=num_cores)(delayed(get_count)(dirname, fname, searchword) for fname in filelist)
                for j,k in occurances: 
                    total_occurances = total_occurances + j 
                    total_words = total_words + k 

                if (total_occurances != 0 and total_words != 0):
                    frequency = float(total_occurances) / total_words
                else:
                    frequency = 0  

                if (frequency > 0):
                    freqs.append(math.log10(frequency))
                else:
                    freqs.append(0)
                dates.append(date)

    session = {}
    sessions = [] 
    for i in range (0, len(freqs)):
        session['date'] = dates[i] 
        session['frequency'] = freqs[i]
        sessions.append(session.copy())
    return sessions

if __name__ == '__main__':
    app.run(debug=True)
