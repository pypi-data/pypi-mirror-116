from CL import config
from importlib import import_module

p = import_module(f"CL.Preprocessor.{config.cnf_dict['pps']}")

NC_FILE_FORMAT = p.NC_FILE_FORMAT
READ_NC_FILE = p.READ_NC_FILE
UPDATE_NC_LIST = p.UPDATE_NC_LIST