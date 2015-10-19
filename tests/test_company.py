import os
import unittest
from project import app, db, bcrypt
from project._config import basedir
from project.models import Company,User

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

    def register_company(self,name,info,website):
        return self.app.post(
            '/create_company/',
            data=dict(name=name,info=info,website=website),
            follow_redirects=True
        )

    def test_users_can_create_company(self):
        self.create_user('Matt McCabe','test@mail.com','python')
        user = User.query.filter_by(email="test@mail.com").first()
        self.create_company('Weyland','we mine stuff','www.test.com',user.id)
        test = db.session.query(Company).all()
        for t in test:
            t.name
        assert t.name == "Weyland"

    def test_create_company_form_present(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        response = self.app.get('/create_company/',follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Create Your Company Profile.',response.data)

    def test_successfuly_create_company_from_form(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        response = self.register_company('Weyland','mining company','wwww.weyland.com')
        self.assertIn(b'Weyland',response.data)

    def test_fail_to_create_company_without_name(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        response = self.register_company('','mining company','wwww.weyland.com')
        self.assertIn(b'This field is required.',response.data)

    def test_create_company_without_info(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        response = self.register_company('Weyland','','wwww.weyland.com')
        self.assertIn(b'Weyland',response.data)

    def test_create_company_without_website(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        response = self.register_company('Weyland','mining company','')
        self.assertIn(b'Thanks for registering your company',response.data)

    def test_delete_company_if_owner(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        self.register_company('Weyland','mining company','www.test.com')
        self.app.get('/company/1/')
        response = self.app.get('/company/1/delete/',follow_redirects=True)
        self.assertIn(b'The company was deleted',response.data)

    def test_fail_to_delete_company_not_owner(self):
        self.register('Matt','McCabe','test@mail.com','python','python')
        self.login('test@mail.com','python')
        self.register_company('Weyland','mining company','www.test.com')
        self.logout()
        self.register('Matt','McCabe','test2@mail.com','python','python')
        self.login('test2@mail.com','python')
        self.app.get('/company/1/')
        response = self.app.get('/company/1/delete/',follow_redirects=True)
        self.assertIn(b'You do not have permission for that',response.data)
