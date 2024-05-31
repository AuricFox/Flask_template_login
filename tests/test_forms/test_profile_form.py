import unittest

from tests.base_test import BaseTestCase_User

from app.forms.profile_form import ProfileForm


class Test_Profile_Form(BaseTestCase_User):

    def test_1_profile_form(self):
        '''
        Tests the inputs for the profile form
        '''
        form = ProfileForm(data={
            'id': '1',
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_2_profile_form(self):
        '''
        Tests for invalid ID field in the profile form
        '''
        form = ProfileForm(data={
            'id': '100',
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())
        self.assertIn('Invalid user ID!', form.id.errors)
    
    #-----------------------------------------------------------------------------------------------------------
    def test_3_profile_form(self):
        '''
        Tests for missing ID field in the profile form
        '''
        form = ProfileForm(data={
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_4_profile_form(self):
        '''
        Tests for missing username field in the profile form
        '''
        form = ProfileForm(data={
            'id': '1',
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_5_profile_form(self):
        '''
        Tests for missing email field in the profile form
        '''
        form = ProfileForm(data={
            'id': '1',
            'username': 'Test User',
            'password': 'Test@User1',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_6_profile_form(self):
        '''
        Tests for missing password field in the profile form
        '''
        form = ProfileForm(data={
            'id': '1',
            'username': 'Test User',
            'email': 'user@testing.com',
            'confirm': 'Test@User1'
        })
        self.assertFalse(form.validate())
        self.assertIn('Password is required!', form.password.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_7_profile_form(self):
        '''
        Tests for missing confirmation password in the profile form
        '''
        form = ProfileForm(data={
            'id': '1',
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'Test@User1'
        })
        self.assertFalse(form.validate())
        self.assertIn('Confirm password is required!', form.confirm.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_8_profile_form(self):
        '''
        Tests for matching passwords in the profile form
        '''
        form = ProfileForm(data={
            'id': '1',
            'username': 'Test User',
            'email': 'user@testing.com',
            'password': 'Test@User1',
            'confirm': 'No1@match'
        })
        self.assertFalse(form.validate())
        self.assertIn('Passwords must match!', form.confirm.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_9_profile_form(self):
        '''
        Tests for duplicate usernames
        '''
        form = ProfileForm(data={
            'id': '2',
            'username': 'Test User1',
            'email': 'testing2@testing.com',
            'password': 'Test@User2',
            'confirm': 'Test@User2'
        })
        self.assertFalse(form.validate())
        self.assertIn('Username already exists!', form.username.errors)

    #-----------------------------------------------------------------------------------------------------------
    def test_10_profile_form(self):
        '''
        Tests for duplicate emails
        '''
        form = ProfileForm(data={
            'id': '2',
            'username': 'Test User2',
            'email': 'user1@testing.com',
            'password': 'Test@User2',
            'confirm': 'Test@User2'
        })
        self.assertFalse(form.validate())
        self.assertIn('Email address already exists!', form.email.errors)


if __name__ == "__main__":
    unittest.main()