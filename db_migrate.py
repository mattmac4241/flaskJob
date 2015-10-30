import sqlite3
from project import db
# from datetime import datetime
from project._config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    db.session.remove()
    db.drop_all()
    db.create_all()
