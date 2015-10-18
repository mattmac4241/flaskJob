from project import db
import datetime
from sqlalchemy.orm import relationship


association_table = db.Table('association_table',
    db.Column('jobs_id', db.Integer, db.ForeignKey('jobs.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String,default="user")
    #applied_to = db.relationship('Job') #Jobs the user applied_to
    applied_to = db.relationship('Job',secondary=association_table,backref=db.backref('jobs', lazy='dynamic'))
    def __init__(self, name=None, email=None, password=None, role=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User {0}>'.format(self.name)

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    info = db.Column(db.String,default='') #used for brief info about company
    website = db.Column(db.String,default='')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self,name=None,info=None,website=None,user_id=None):
        self.name = name
        self.info = info
        self.website = website
        self.user_id = user_id

    def __repr__(self):
        return '<Comapny {0}>'.format(self.name)


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=False)
    description = db.Column(db.String,default='')
    salary = db.Column(db.Integer)
    zip_code = db.Column(db.String)
    job_type = db.Column(db.String,default='') #reprsents Fulltime,partime,contract,internship,commission
    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'))

    def __init__(self,title=None,description=None,salary=None,zip_code=None,job_type=None,company_id=None):
        self.title = title
        self.description = description
        self.salary = salary
        self.zip_code = zip_code
        self.job_type = job_type
        self.company_id = company_id

    def __repr__(self):
        return '<Job {0}>'.format(self.title)
