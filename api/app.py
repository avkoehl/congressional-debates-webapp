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

    os.system("/usr/local/bin/python3.5 frequency.py" + " " +  word + " " + str(30))
    myfile = open("./outputs/" + word + ".txt", "r")
    result = myfile.read()
    return (result);


@app.route('/distribution', methods=['GET'])
def get_distribution():
    word = request.args.get('word', type = str).lower()

    os.system("/usr/local/bin/python3.5 distributional.py" + " " +  word + " " + str(30))
    myfile = open("./outputs/dist" + word + ".txt", "r")
    result = myfile.read()
    return (result);




if __name__ == '__main__':
    app.run(debug=True)

