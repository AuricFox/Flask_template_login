from flask_testing import TestCase
from datetime import datetime

from app import init_app
from app.extensions import db
from app.models.user import User
from app.models.default import Default_Model

class BaseTestCase(TestCase):
    '''
    Creates a base test class for cases that don't use any models
    '''
    def create_app(self):
        # Create and configure the app for testing
        app = init_app('config.TestingConfig')
        return app

    def setUp(self):
        # Set up the database
        self.client = self.app.test_client()
        db.create_all()  

    def tearDown(self):
        # Tear down the database
        db.session.remove()
        db.drop_all()


class BaseTestCase_User(BaseTestCase):
    '''
    Creates a base test class for cases using the user model
    '''
    def create_app(self):
        # Create and configure the app for testing
        app = init_app('config.TestingConfig')
        return app

    def setUp(self):
        # Set up the database
        super().setUp()
        self.create_test_users()

    def create_test_users(self):
        # Populates the database with test date
        self.user1 = User(username='Test User1', email='user1@testing.com', password='Test@User1')
        self.user2 = User(username='Test User2', email='user2@testing.com', password='Test@User2')
        self.admin = User(username='Test Admin', email='admin@testing.com', password='Test@Admin1', is_admin=True)
        
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.add(self.admin)
        db.session.commit()


class BaseTestCase_Models(BaseTestCase):
    '''
    Creates a base test class for cases using the default and user models
    '''
    def setUp(self):
        # Set up the database
        super().setUp()
        self.create_test_data()

    def create_test_data(self):
        # Populates the database with test date
        self.default1 = Default_Model(
            name='Test Name', 
            date=datetime.strptime('2024-05-29', '%Y-%m-%d'), 
            message='This is a base test message!'
        )
        self.admin = User(username='Test Admin', email='admin@testing.com', password='Test@Admin1', is_admin=True)
        
        db.session.add(self.default1)
        db.session.add(self.admin)
        db.session.commit()