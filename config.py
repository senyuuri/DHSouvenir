# config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'dhs.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'natsuyuu'

DATABASE_PATH = os.path.join(basedir, DATABASE)