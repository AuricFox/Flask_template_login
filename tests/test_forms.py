import unittest

from base_test import BaseTestCase

from app.forms.default_form import DefaultForm
from app.forms.login_form import LoginForm
from app.forms.profile_form import ProfileForm
from app.forms.register_form import RegisterForm
from app.forms.user_form import UserForm

# ==============================================================================================================
class Test_Default_Form(BaseTestCase):

    def test_1_default_form(self):
        '''
        Tests the input for the default form
        '''
        form = DefaultForm(data={
            'name': 'Test User',
            'date': '2024-05-23',
            'message': 'This is a test message from the unit testing.'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_2_default_form(self):
        '''
        Test for invalid date format inputs into the default form
        '''
        form = DefaultForm(data={
            'name': 'Test User',
            'date': '23-05-2024',
            'message': 'The invalid date is reversed.'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_3_defaault_form(self):
        '''
        Test for invalid date inputs into the default form
        '''
        form = DefaultForm(data={
            'name': 'Test User',
            'date': 'NOT A DATE',
            'message': 'The invalid date is not a date!'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_4_default_form(self):
        '''
        Test for no date inputs into the default form
        '''
        form = DefaultForm(data={
            'name': 'Test User',
            'message': 'There is no date!'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_5_default_form(self):
        '''
        Test for absent name input into the default form
        '''
        form = DefaultForm(data={
            'date': '2024-05-23',
            'message': 'There is no name!'
        })
        self.assertFalse(form.validate())
    
    #-----------------------------------------------------------------------------------------------------------
    def test_6_default_form(self):
        '''
        Test for invalid message inputs into the default form
        '''
        long_message = 'A' * 1002

        form = DefaultForm(data={
            'name': 'Test User',
            'date': '2024-05-23',
            'message': long_message
        })
        self.assertFalse(form.validate())

# ==============================================================================================================
class Test_Login_form(BaseTestCase):

    def test_1_login_form(self):
        '''
        Tests the inputs of the login form
        '''
        form = LoginForm(data={
            'username': 'Test User',
            'password': 'Test@User1'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_2_login_form(self):
        '''
        Tests for missing username
        '''
        form = LoginForm(data={
            'password': 'Test@User1'
        })
        self.assertFalse(form.validate())
    
    #-----------------------------------------------------------------------------------------------------------
    def test_3_login_form(self):
        '''
        Tests for missing password
        '''
        form = LoginForm(data={
            'username': 'Test User'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_4_login_form(self):
        '''
        Tests for usernames that are less than 6 characters
        '''
        form = LoginForm(data={
            'username': 'Test',
            'password': 'Test@User1'
        })
        self.assertFalse(form.validate())
    
    #-----------------------------------------------------------------------------------------------------------
    def test_5_login_form(self):
        '''
        Tests for usernames that are more than 100 characters
        '''
        form = LoginForm(data={
            'username': 'T' * 102,
            'password': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_6_login_form(self):
        '''
        Tests for passwords that are less than 8 characters
        '''
        form = LoginForm(data={
            'username': 'Test User',
            'password': 'T@u1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_7_login_form(self):
        '''
        Tests for passwords that are more than 100 characters
        '''
        form = LoginForm(data={
            'username': 'T' * 102,
            'password': 'T@1' + 't' * 99
        })
        self.assertFalse(form.validate())


if __name__ == "__main__":
    unittest.main()