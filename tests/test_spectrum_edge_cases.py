
import pytest
import json
import pickle 

import base64
import pandas as pd
import numpy as np

import collections 

@pytest.fixture
def spectrum_test_meta():
    """return request meta information for /spectrum tets"""
    mimetype = 'application/json'

    return {
        'url': '/spectrum',
        'post': {
            'mimetype': mimetype,
            'headers': {
                'Content-Type': mimetype,
                'Accept': mimetype
            }
        }
    }

@pytest.fixture
def spectrum_test_data():
    """return test data values for /spectrum tets"""
    # Commented out this time series as the endpoint does not 
    # accept a proper time series.  Instead it appears to only
    # accept a simple vector
    # index = pd.DatetimeIndex(['2020-07-04', '2020-08-04',
    #                      '2020-09-04', '2020-10-04'])
    # ts = pd.Series([0, 1, 2, 3], index=index)
    ts = np.arange(4, dtype=np.float64)
    jsonSafe = ts #pickle.dumps(ts)
    s = base64.b64encode(jsonSafe).decode('ascii')
 
    success_data = {
        'spectrum': s,
        'sampling_rate': 1, 
        'units': 1,
        'dtype': 'float64'
    }

    broken_spectrum = {
        'spectrum': ['a', 'b'],
        'sampling_rate': 1, 
        'units': 1,
        'dtype': 'float64'
    }

    broken_sampling_rate = {
        'spectrum': ['a', 'b'],
        'sampling_rate': 'a', 
        'units': 1,
        'dtype': 'float64'
    }

    return {
        'success_data': success_data,
        'broken_spectrum': broken_spectrum,
        'broken_sampling_rate': broken_sampling_rate
    }

def test_spectrum_simple_success(client, spectrum_test_meta, spectrum_test_data):
    """Provide simple spectrum vector to generate a successful spectrum calculation"""
    response = client.post(
        spectrum_test_meta['url'],
        data=json.dumps(spectrum_test_data['success_data']),
        headers=spectrum_test_meta['post']['headers'])
    assert collections.Counter(response.json['spectrum']) == collections.Counter(np.arange(4, dtype=np.float64)) 

def test_spectrum_broken_spectrum(client, spectrum_test_meta, spectrum_test_data):
    """Provide a simple spectrum vector with a values that cannot be converted into timeseries"""
    response = client.post(
        spectrum_test_meta['url'],
        data=json.dumps(spectrum_test_data['broken_spectrum']),
        headers=spectrum_test_meta['post']['headers'])
    assert response.mimetype == 'application/json'
    assert response.status_code == 500

def test_spectrum_broken_sampling_rate(client, spectrum_test_meta, spectrum_test_data):
    """Provide a sampling rate that cannot be cast to float"""
    response = client.post(
        spectrum_test_meta['url'],
        data=json.dumps(spectrum_test_data['broken_sampling_rate']),
        headers=spectrum_test_meta['post']['headers'])
    assert response.mimetype == 'application/json'
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid Sampling Rate'