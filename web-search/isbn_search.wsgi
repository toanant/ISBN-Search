#!/usr/bin/python
import os, sys

PROJECT_PATH = os.path.abspath(os.path.dirname( __file__ ))

venv = os.path.abspath('/home/ubuntu/.virtualenvs/isbn/bin/activate_this.py')
execfile(venv, dict(__file__=venv))

sys.path.insert(0, PROJECT_PATH)

from web import app as application
