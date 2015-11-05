from project import db,app
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import SearchQueryMixin

association_table = db.Table('association_table',
    db.Column('jobs_id', db.Integer, db.ForeignKey('jobs.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)
company_table = db.Table('company_table',
    db.Column('jobs_id', db.Integer, db.ForeignKey('jobs.id')),
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id'))
)
user_table = db.Table('user_table',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id'))
)

make_searchable()
db.configure_mappers()
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String,default="user")
    applied_to = db.relationship('Job',secondary=association_table,backref=db.backref('jobs', lazy='dynamic'))
    companies = db.relationship('Company',secondary=user_table,backref=db.backref('companies', lazy='dynamic'))
    profile_picture = db.Column(db.String,default="static/files/users/default/default_profile.png")


    def __init__(self, name=None, email=None, password=None, role=None,profile_picture=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.profile_picture = profile_picture

    def __repr__(self):
        return '<User {0}>'.format(self.name)


class CompanyQuery(BaseQuery, SearchQueryMixin):
    pass

class Company(db.Model):
    query_class = CompanyQuery
    __tablename__ = 'companies'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    info = db.Column(db.String,default='') #used for brief info about company
    website = db.Column(db.String,default='')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    jobs_posted = db.relationship('Job',secondary=company_table)
    profile_picture = db.Column(db.String,default='static/files/users/default/default_profile.png')
    search_vector = db.Column(TSVectorType('name', 'info'))

    def __init__(self,name=None,info=None,website=None,user_id=None,profile_picture=None):
        self.name = name
        self.info = info
        self.website = website
        self.user_id = user_id
        self.profile_picture = profile_picture

    def __repr__(self):
        return '<Comapny {0}>'.format(self.name)

class JobQuery(BaseQuery, SearchQueryMixin):
    pass

class Job(db.Model):
    query_class = JobQuery
    __tablename__ = 'jobs'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=False)
    description = db.Column(db.String,default='')
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    salary = db.Column(db.Integer)
    zip_code = db.Column(db.String)
    job_type = db.Column(db.String,default='') #reprsents Fulltime,partime,contract,internship,commission
    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'))
    applicants = db.relationship('User',secondary=association_table,backref=db.backref('users', lazy='dynamic'))
    search_vector = db.Column(TSVectorType('title', 'description'))


    def __init__(self,title=None,description=None,salary=None,zip_code=None,job_type=None,company_id=None):
        self.title = title
        self.description = description
        self.salary = salary
        self.zip_code = zip_code
        self.job_type = job_type
        self.company_id = company_id

    def __repr__(self):
        return '<Job {0}>'.format(self.title)
