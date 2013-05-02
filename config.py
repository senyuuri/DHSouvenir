# config.py
import os
import inconfig
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'dhs.db'


DATABASE_PATH = os.path.join(basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

OPENID_PROVIDERS = [
	    			{ 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
	    			{ 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
	    			{ 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
	    			{ 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

