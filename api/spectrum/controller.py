import base64
import numpy as np
import pandas as pd 

from flask import request
from api import app


@app.route('/spectrum', methods=['GET'])
def getSpectrum():
    """
    Spectrum get request will respond with the post paramaters expected by the post request.
    """
    return {'params': ['sampling_rate', 'units', 'dtype']}

@app.route('/spectrum', methods=['POST'])
def postSpectrum():
    """
    Spectrum post request will transform the data vector into a time series and then 
    use FFT to provide the frequency domain.

    See get request for post params. 
    """
    try:
        req = request.get_json()
        try:
            #sampling frequency
            sr = float(req['sampling_rate'])
        except:
            #raise Exception("sample_rate", "Only floats are allowed") 
            return {'error': 'Invalid Sampling Rate'}, 400
        # Still have no clue what this is used for
        units = req["units"]

        dtype = req['dtype'] if 'dtype' in req else "float64"
        spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
        spectrum_series = pd.Series(spectrum)

        samples_per_signal = len(spectrum)
        duration = samples_per_signal / sr

        freq_domain = np.fft.fft(spectrum_series) #/duration # fft computing and normalization
        freq_range = duration/sr

        # base 64 encode to ensure the response is json safe
        return {
            'spectrum': base64.b64encode(freq_domain).decode('ascii'),
            'freq_range': freq_range
        }
    except:
        # Log error
        
        error = app.response_class(
            response={'error': 'Internal server error'},
            status=500,
            mimetype='application/json'
        )   
        return error