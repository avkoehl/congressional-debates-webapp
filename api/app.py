from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from frequency import *
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/frequency', methods=['GET'])
def get_frequency():
    word = request.args.get('word', type = str)
    freq_array = frequency(word)
    response = jsonify(freq_array)
    return response;


if __name__ == '__main__':
    app.run(debug=True)
