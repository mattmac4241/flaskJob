from project import db
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String,default="user")

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,name=None,user_id=None):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<Comapny {0}>'.format(self.name)


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    salary = db.Column(db.Integer)
    zip_code = db.Column(db.Integer)
    job_type = db.Column(db.String) #reprsents Fulltime,partime,contract,internship,commission
    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'))

    def __init__(self,name=None,description=None,salary=None,zip_code=None,job_type,company_id=None):
        self.name = name
        self.description = description
        self.salary = salary
        self.zip_code = zip_code
        self.job_type = job_type
        self.company_id = company_id
