from CL import config
from importlib import import_module

m = import_module(f"CL.Machine.{config.cnf_dict['machine']}")

A_CENTER_Z = m.A_CENTER_Z
HEAD_HEIGHT = m.HEAD_HEIGHT
A_AIX1 = m.A_AIX1
C_AIX1 = m.C_AIX1
A_MODEL = m.A_MODEL
C_MODEL = m.C_MODEL
A_NAME = m.A_NAME
C_NAME = m.C_NAME
COLOR = m.COLOR
