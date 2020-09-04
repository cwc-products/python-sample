import base64

from flask import Flask, request
import numpy as np


app = Flask(__name__)

@app.route('/')
def routes():
    return {
        "spectrum": "/spectrum",
        "mean": "/mean",
        "median": "/median",
    }

import api.spectrum.controller

@app.route('/mean', methods=['POST', 'GET'])
def mean():
    if request.method == 'GET':
        return {'params': ['dtype']}

    req = request.get_json()
    dtype = req['dtype'] if 'dtype' in req else "float64"
    spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
    samples_per_signal = len(spectrum)
    return {'mean': np.mean(spectrum)}

@app.route('/median', methods=['POST', 'GET'])
def median():
    if request.method == 'GET':
        return {'params': ['dtype']}

    req = request.get_json()
    dtype = req['dtype'] if 'dtype' in req else "float64"
    spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
    samples_per_signal = len(spectrum)
    return {'median': np.median(spectrum)}


def create_app():
    return app
