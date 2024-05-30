import unittest

from tests.base_test import BaseTestCase_User

from app.forms.login_form import LoginForm


class Test_Login_form(BaseTestCase_User):

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