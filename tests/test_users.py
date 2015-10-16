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
        return self.app.post('/', data=dict(
            email=emil, password=password), follow_redirects=True)

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

if __name__ == "__main__":
    unittest.main()
