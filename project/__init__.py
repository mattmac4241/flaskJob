# project/__init__.py
import datetime
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from project.users.views import users_blueprint
from project.companies.views import companies_blueprint
from project.jobs.views import jobs_blueprint
from project.search.views import search_blueprint


app.register_blueprint(users_blueprint)
app.register_blueprint(companies_blueprint)
app.register_blueprint(jobs_blueprint)
app.register_blueprint(search_blueprint)
