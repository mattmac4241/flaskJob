# project/_config.py
import os


# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'jobs.db'
CSRF_ENABLED = True
SECRET_KEY = '5fb730df-856b-4c9e-883c-8387472a7ef0'
DEBUG = True

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = "postgresql://matt:Password@localhost/jobs"

ALLOWED_EXTENSIONS = set(['jpg','png'])
UPLOAD_FOLDER = '%s/static/files/users/' % basedir
