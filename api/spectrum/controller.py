from flask import request

from api import app

@app.route('/spectrum', methods=['GET'])
def getSpectrum():
    return {'params': ['sampling_rate', 'units', 'dtype']}

@app.route('/spectrum', methods=['POST'])
def postSpectrum():
    req = request.get_json()
    sr = float(req['sampling_rate'])
    units = req["units"]
    dtype = req['dtype'] if 'dtype' in req else "float64"
    spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
    samples_per_signal = len(spectrum)
    duration = samples_per_signal / sr
    return {'spectrum': spectrum}