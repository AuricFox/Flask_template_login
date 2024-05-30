import unittest

from tests.base_test import BaseTestCase_User

from app.forms.user_form import UserForm
from app.models.user import User

class Test_User_Form(BaseTestCase_User):

    def test_1_user_form(self):
        '''
        Tests the inputs for the user form
        '''
        user = User.query.filter_by(username='Test User1').first()

        form = UserForm(data={
            'id': user.id,
            'username': 'Test User',
            'email': 'testing@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1',
            'is_admin': 'False'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_2_user_form(self):
        '''
        Tests for invalid ID field in the user form
        '''
        form = UserForm(data={
            'id': '100',
            'username': 'Test User',
            'email': 'testing@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1',
            'is_admin': 'False'
        })
        self.assertFalse(form.validate())
        self.assertIn('Invalid user ID!', form.id.errors)
    
    #-----------------------------------------------------------------------------------------------------------
    def test_3_user_form(self):
        '''
        Tests for missing ID field in the user form
        '''
        form = UserForm(data={
            'username': 'Test User',
            'email': 'testing@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1',
            'is_admin': 'False'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_4_user_form(self):
        '''
        Tests for missing username field in the user form
        '''
        user = User.query.filter_by(username='Test User1').first()

        form = UserForm(data={
            'id': user.id,
            'email': 'testing@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1',
            'is_admin': 'False'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_5_user_form(self):
        '''
        Tests for missing email field in the user form
        '''
        user = User.query.filter_by(username='Test User1').first()

        form = UserForm(data={
            'id': user.id,
            'username': 'Test User',
            'password': 'Test@User1',
            'confirm': 'Test@User1',
            'is_admin': 'False'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_6_user_form(self):
        '''
        Tests for missing password field in the user form
        '''
        user = User.query.filter_by(username='Test User1').first()

        form = UserForm(data={
            'id': user.id,
            'username': 'Test User',
            'email': 'testing@testing.com',
            'confirm': 'Test@User1',
            'is_admin': 'False'
        })
        self.assertFalse(form.validate())
        self.assertIn('Password is required!', form.password.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_7_user_form(self):
        '''
        Tests for missing confirmation password in the user form
        '''
        user = User.query.filter_by(username='Test User1').first()

        form = UserForm(data={
            'id': user.id,
            'username': 'Test User',
            'email': 'testing@testing.com',
            'password': 'Test@User1',
            'is_admin': 'False'
        })
        self.assertFalse(form.validate())
        self.assertIn('Confirm password is required!', form.confirm.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_8_user_form(self):
        '''
        Tests for matching passwords in the user form
        '''
        user = User.query.filter_by(username='Test User1').first()

        form = UserForm(data={
            'id': user.id,
            'username': 'Test User',
            'email': 'testing@testing.com',
            'password': 'Test@User1',
            'confirm': 'No1@match',
            'is_admin': 'False'
        })
        self.assertFalse(form.validate())
        self.assertIn('Passwords must match!', form.confirm.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_9_user_form(self):
        '''
        Tests for duplicate usernames
        '''
        user2 = User.query.filter_by(username='Test User2').first()

        form = UserForm(data={
            'id': user2.id,
            'username': 'Test User1',
            'email': 'testing2@testing.com',
            'password': 'Test@User2',
            'confirm': 'Test@User2',
            'is_admin': 'False'
        })
        self.assertFalse(form.validate())
        self.assertIn('Username already exists!', form.username.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_10_user_form(self):
        '''
        Tests for duplicate emails
        '''
        user2 = User.query.filter_by(username='Test User2').first()

        form = UserForm(data={
            'id': user2.id,
            'username': 'Test User2',
            'email': 'user1@testing.com',
            'password': 'Test@User2',
            'confirm': 'Test@User2',
            'is_admin': 'False'
        })
        self.assertFalse(form.validate())
        self.assertIn('Email address already exists!', form.email.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_11_user_form(self):
        '''
        Tests for all optional fields removed
        '''
        user = User.query.filter_by(username='Test User1').first()

        form = UserForm(data={
            'id': user.id
        })
        self.assertTrue(form.validate())

if __name__ == "__main__":
    unittest.main()