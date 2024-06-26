import unittest

from tests.base_test import BaseTestCase_User

from app.forms.base_form import RegisterForm


class Test_Register_form(BaseTestCase_User):

    def test_1_register_form(self):
        '''
        Tests the inputs of the register form
        '''
        form = RegisterForm(data={
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_2_register_form(self):
        '''
        Tests missing username field from the register form
        '''
        form = RegisterForm(data={
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_3_register_form(self):
        '''
        Tests missing email field from the register form
        '''
        form = RegisterForm(data={
            'username': 'Test User',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_4_register_form(self):
        '''
        Tests missing password field from the register form
        '''
        form = RegisterForm(data={
            'username': 'Test User',
            'email': 'user@testing.com',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_5_register_form(self):
        '''
        Tests missing confirm field from the register form
        '''
        form = RegisterForm(data={
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_6_register_form(self):
        '''
        Tests for usernames less then 6 characters
        '''
        form = RegisterForm(data={
            'username': 'Test',
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_7_register_form(self):
        '''
        Tests for usernames with more than 100 characters
        '''
        form = RegisterForm(data={
            'username': 'T' * 102,
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())

     #-----------------------------------------------------------------------------------------------------------
    def test_8_register_form(self):
        '''
        Tests for passwords less then 8 characters
        '''
        form = RegisterForm(data={
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'T@u1',
            'confirm': 'T@u1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_9_register_form(self):
        '''
        Tests for passwords with more than 100 characters
        '''
        form = RegisterForm(data={
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'T@u1' + 't' * 100,
            'confirm': 'T@u1' + 't' * 100
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_9_register_form(self):
        '''
        Tests for matching password and confirmation password
        '''
        form = RegisterForm(data={
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Mismatch@User1'
        })
        self.assertFalse(form.validate())
    
    #-----------------------------------------------------------------------------------------------------------
    def test_10_register_form(self):
        '''
        Tests for duplicate usernames
        '''
        form = RegisterForm(data={
            'username': 'Test User2',
            'email': 'user@testing.com',
            'password': 'Test@User2',
            'confirm': 'Test@User2'
        })
        self.assertFalse(form.validate())
        self.assertIn('Username already exists!', form.username.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_11_register_form(self):
        '''
        Tests for duplicate emails
        '''
        form = RegisterForm(data={
            'username': 'Test User',
            'email': 'user2@testing.com',
            'password': 'Test@User2',
            'confirm': 'Test@User2'
        })
        self.assertFalse(form.validate())
        self.assertIn('Email address already exists!', form.email.errors)


if __name__ == "__main__":
    unittest.main()