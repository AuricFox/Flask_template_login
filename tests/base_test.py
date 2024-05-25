from flask_testing import TestCase

from app import init_app
from app.extensions import db

class BaseTestCase(TestCase):
    def create_app(self):
        # Create and configure the app for testing
        app = init_app('config.TestingConfig')
        return app

    def setUp(self):
        # Set up the database
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        # Tear down the database
        db.session.remove()
        db.drop_all()