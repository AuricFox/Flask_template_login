from flask_testing import TestCase

from app import init_app
from app.extensions import db
from app.models.user import User

class BaseTestCase(TestCase):
    def create_app(self):
        # Create and configure the app for testing
        app = init_app('config.TestingConfig')
        return app

    def setUp(self):
        # Set up the database
        db.create_all()
        self.client = self.app.test_client()

        self.user1 = User(username='Test User1', email='user1@testing.com', password='Test@User1')
        self.user2 = User(username='Test User2', email='user2@testing.com', password='Test@User2')
        
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

    def tearDown(self):
        # Tear down the database
        db.session.remove()
        db.drop_all()