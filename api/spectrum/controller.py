import base64
import numpy as np

from flask import request
from api import app

# Spectrum get request will respond with the post paramaters expected by the post request.
@app.route('/spectrum', methods=['GET'])
def getSpectrum():
    return {'params': ['sampling_rate', 'units', 'dtype']}

@app.route('/spectrum', methods=['POST'])
def postSpectrum():
    try:
        req = request.get_json()
        try:
            sr = float(req['sampling_rate'])
        except:
            #raise Exception("sample_rate", "Only floats are allowed") 
            return {'error': 'Invalid Sampling Rate'}, 400
        units = req["units"]
        dtype = req['dtype'] if 'dtype' in req else "float64"
        spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
        samples_per_signal = len(spectrum)
        duration = samples_per_signal / sr
        return {'spectrum': spectrum}
    except:
        # Log error
        
        error = app.response_class(
            response={'error': 'Internal server error'},
            status=500,
            mimetype='application/json'
        )   
        return error