import os
import unittest
from project import app, db, bcrypt
from project._config import basedir
from project.models import Company,User,Job
from flask import url_for

TEST_DB = 'test.db'

class ComapnyTest(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.assertEquals(app.debug, False)
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #HELPER FUNCTIONS
    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email, password=password), follow_redirects=True)

    def register(self, first_name,last_name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(first_name=first_name,last_name=last_name,email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def register_company(self,name,info,website):
        return self.app.post(
            '/create_company/',
            data=dict(name=name,info=info,website=website),
            follow_redirects=True
        )

    #create a job seeker account
    def create_user(self,name,email,password):
        new_user = User(
            name=name,
            email=email,
            password=bcrypt.generate_password_hash(password),
        )
        db.session.add(new_user)
        db.session.commit()

    def create_company(self,name,info,website,user_id):
        new_company = Company(
            name=name,
            info=info,
            website=website,
            user_id=user_id
        )
        db.session.add(new_company)
        db.session.commit()

    def create_job(self,name,description,salary,zip_code,job_type,company_id):
        new_job = Job(
            name = name,
            description = description,
            salary = salary,
            zip_code = zip_code,
            job_type = job_type,
            company_id = company_id
        )
        db.session.add(new_job)
        db.session.commit()

    def post_job(self,name,description,salary,zip_code,job_type):
        return self.app.post(
            '/create_company/',
            data=dict(name=name,info=info,website=website),
            follow_redirects=True
        )

    def test_job_creation(self):
        self.create_user("Matthew McCabe","test@mail.com",'python')
        self.create_company("weyland",'mines','www.test.com',1)
        self.create_job("miner",'you will work the mines','50,000',60453,'',1)
        test = db.session.query(Job).all()
        for t in test:
            t.name
        assert t.name == "miner"

    def test_successfully_post_job(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        self.register_company('weyland','mining company','wwww.weyland.com')
        response = self.app.get(url_for('/company/1/create_job'),follow_redirects=True)
        self.assertIn('Thanks for posting a job',response.data)

    def test_fail_job_post_because_not_owner(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        self.register_company('weyland','mining company','wwww.weyland.com')
        self.logout()
        self.register('Fake','Name','test2@mail.com','python','python')
        self.login('test2@mail.com','python')
        response = self.app.get('/company/1/create_job/',follow_redirects=True)
        self.assertEqual(response.status_code,403)
