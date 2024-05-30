import unittest

from flask import url_for
from flask_login import current_user

from tests.base_test import BaseTestCase_User

class Test_Login(BaseTestCase_User):

    def test_login_page(self):
        '''
        Tests the retrieval of the login page
        '''
        with self.client:

            response = self.client.get(url_for('auth.login'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login", response.data)
    # ==============================================================================================================
    def test_logging_in(self):
        '''
        Tests the retrieval of the login page
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.login'), 
                data = dict(username='Test Admin', password='Test@Admin1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertIn(b"Home", response.data)
    # ==============================================================================================================
    def test_failed_log_in(self):
        '''
        Tests invalid login
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.login'), 
                data = dict(username='Test User', password='Test@nonuser1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"Login", response.data)
    # ==============================================================================================================
    def test_log_out(self):
        '''
        Tests the logout
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.login'), 
                data = dict(username='Test Admin', password='Test@Admin1'),
                follow_redirects=True
            )

            response = self.client.get(
                url_for('auth.log_out', follow_redirects=True)
            )

            self.assertEqual(response.status_code, 302)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"home", response.data)


class Test_Sign_up(BaseTestCase_User):

    def test_signup_page(self):
        '''
        Tests the retrieval of the registration page
        '''
        with self.client:

            response = self.client.get(url_for('auth.sign_up'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Sign Up", response.data)
    # ==============================================================================================================
    def test_1_signup_page(self):
        '''
        Tests normal user registration
        '''
        with self.client:
            
            response = self.client.post(
                url_for('auth.sign_up'), 
                data = dict(username='Test User', email='testuser@testing.com', password='Test@User1', confirm='Test@User1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertIn(b"home", response.data)
    # ==============================================================================================================
    def test_2_signing_up(self):
        '''
        Tests for duplicate usernames during registration
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.sign_up'), 
                data = dict(username='Test User1', email='testuser1@testing.com', password='Test@User1', confirm='Test@User1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"Sign Up", response.data)
    # ==============================================================================================================
    def test_3_signing_up(self):
        '''
        Tests for duplicate emails during registration
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.sign_up'), 
                data = dict(username='Test User', email='user1@testing.com', password='Test@User1', confirm='Test@User1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"Sign Up", response.data)
    # ==============================================================================================================
    def test_4_signing_up(self):
        '''
        Tests for missing username during registration
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.sign_up'), 
                data = dict(email='testuser1@testing.com', password='Test@User1', confirm='Test@User1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"Sign Up", response.data)
    # ==============================================================================================================
    def test_5_signing_up(self):
        '''
        Tests for missing email during registration
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.sign_up'), 
                data = dict(username='Test User', password='Test@User1', confirm='Test@User1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"Sign Up", response.data)
    # ==============================================================================================================
    def test_6_signing_up(self):
        '''
        Tests for missing password during registration
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.sign_up'), 
                data = dict(username='Test User', email='testuser@testing.com', confirm='Test@User1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"Sign Up", response.data)
    # ==============================================================================================================
    def test_7_signing_up(self):
        '''
        Tests for missing confirmation password during registration
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.sign_up'), 
                data = dict(username='Test User', email='testuser@testing.com', password='Test@User1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"Sign Up", response.data)
    # ==============================================================================================================
    def test_8_signing_up(self):
        '''
        Tests for mismatching passwords during registration
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.sign_up'), 
                data = dict(username='Test User', email='testuser@testing.com', password='Test@User1', confirm='notTest@User1'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b"Sign Up", response.data)

if __name__ == "__main__":
    unittest.main()