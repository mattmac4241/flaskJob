import os
import unittest

from project import app, db, bcrypt
from project._config import basedir
from project.models import User

TEST_DB = 'test.db'

class UsersTest(unittest.TestCase):
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

    def test_users_can_register(self):
        new_user = User("Matt McCabe","mattmac4241@gmail.com","home2222")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "Matt McCabe"

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Please sign in to access your task list',response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('/register/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Please register to access the task list',response.data)

    def test_user_can_login(self):
        self.register("Matthew",'McCabe','mattmac4241@yahoo.com','testpassword','testpassword')
        response = self.login('mattmac4241@yahoo.com','testpassword')
        self.assertIn('Matthew McCabe',response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_invalid_form_data(self):
        self.register("Matthew","McCabe","test@mail.com",'python','python')
        response = self.login('alert("alert box");','foo')
        self.assertIn(b'Invalid username or password.',response.data)

    def test_login_with_incorrect_password(self):
        self.register("Matthew","McCabe","test@mail.com",'python','python')
        response = self.login('test@gmail','sdfsdfs')
        self.assertIn(b'Invalid username or password.',response.data)

    def test_login_with_incorrect_email(self):
        self.register("Matthew","McCabe","test@mail.com",'python','python')
        response = self.login('fake@mail.com','python')
        self.assertIn(b'Invalid username or password.',response.data)

    def test_register_user_already_registered(self):
        self.app.get('register/',follow_redirects=True)
        self.register("Matthew","McCabe","test@mail.com",'python','python')
        self.app.get('register/',follow_redirects=True)
        response = self.register("Matthew","McCabe","test@mail.com",'python','python')
        self.assertIn(
            b'That username and/or email alread exists',
            response.data
        )
    def test_register_user_with_no_email(self):
        self.app.get('register/',follow_redirects=True)
        response = self.register("Matthew","McCabe",'','python','python')
        self.assertIn('This field is required.',response.data)

    def test_register_user_with_no_first_name(self):
        self.app.get('register/',follow_redirects=True)
        response = self.register("","McCabe",'test@email.com','python','python')
        self.assertIn('This field is required.',response.data)

    def test_register_user_with_no_last_name(self):
        self.app.get('register/',follow_redirects=True)
        response = self.register("Matthew","",'test@email.com','python','python')
        self.assertIn('This field is required.',response.data)

    def test_register_with_no_password(self):
        self.app.get('register/',follow_redirects=True)
        response = self.register("Matthew","McCabe",'test@email.com','','python')
        self.assertIn('This field is required.',response.data)

    def test_register_with_no_confirm_password(self):
        self.app.get('register/',follow_redirects=True)
        response = self.register("Matthew","McCabe",'test@email.com','python','')
        self.assertIn('This field is required.',response.data)

    def test_register_with_no_confirm_password(self):
        self.app.get('register/',follow_redirects=True)
        response = self.register("Matthew","McCabe",'test@email.com','python','pthonds')
        self.assertIn('Field must be equal to password.',response.data)


if __name__ == "__main__":
    unittest.main()
