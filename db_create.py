# db_create.py


from project import db
from sqlalchemy.orm.mapper import configure_mappers


configure_mappers()
# create the database and the db table
db.create_all()


# commit the changes
db.session.commit()
