import os
import pickle

cnf_dict = {}

if os.path.exists('config.cnf'):
    with open('config.cnf', 'rb') as f:
        cnf_dict = pickle.load(f)
else:
    cnf_dict['machine'] = "hans_5axis"
    cnf_dict['pps'] = "hans_5axis_siemens"
    cnf_dict['pps'] = "hans_5axis_beckhoff"


