import unittest

from flask import url_for
from flask_login import current_user

from tests.base_test import BaseTestCase_User

# ==============================================================================================================
# TEST MAIN PROFILE PAGE
# ==============================================================================================================
class Test_Profile_Page(BaseTestCase_User):

    def test_1_profile_page(self):
        '''
        Tests the profile page with successful login
        '''
        response = self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )

        response = self.client.get(url_for('profile.index'), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>View Profile</title>", response.data)
    # ==============================================================================================================
    def test_2_profile_page(self):
        '''
        Tests the profile page with no login
        '''
        response = self.client.get(url_for('profile.index'), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
# ==============================================================================================================
# TEST PROFILE EDIT PAGE
# ==============================================================================================================
class Test_profile_Edit_Page(BaseTestCase_User):

    def test_1_profile_edit_page(self):
        '''
        Tests the edit profile page with login
        '''
        response = self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )        

        response = self.client.get(url_for('profile.edit_profile'), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Edit Profile</title>", response.data)
    # ==============================================================================================================
    def test_2_profile_edit_page(self):
        '''
        Tests the profile edit page without login
        '''
        response = self.client.get(url_for('profile.edit_profile'), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    # ==============================================================================================================
    def test_3_profile_edit_page(self):
        '''
        Tests the admin update post with login
        '''
        # Admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test User1', password='Test@User1'),
            follow_redirects=True
        )        

        response = self.client.post(
            url_for('profile.edit_profile'), 
            data={
                'id': '1',
                'username': 'Update Profile',
                'email': 'updateuser@testing.com',
                'password': 'Update@user1',
                'confirm': 'Update@user1'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>View Profile</title>", response.data)
    # ==============================================================================================================
    def test_4_profile_edit_page(self):
        '''
        Tests the profile post without login
        '''
        response = self.client.post(
            url_for('profile.edit_profile'), 
            data={
                'id': '1',
                'username': 'Update User',
                'email': 'updateuser@testing.com',
                'password': 'Update@user1',
                'confirm': 'Update@user1'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    # ==============================================================================================================
    def test_5_profile_edit_page(self):
        '''
        Tests the profile post with missing optional fields
        '''
        # Admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test User1', password='Test@User1'),
            follow_redirects=True
        )        

        response = self.client.post(
            url_for('profile.edit_profile'), 
            data={
                'id': '1',
                'username': 'Update User',
                'email': 'updateuser@testing.com'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>View Profile</title>", response.data)
# ==============================================================================================================
# TEST PROFILE DELETE ROUTE
# ==============================================================================================================
class Test_Profile_Delete_Route(BaseTestCase_User):

    def test_1_profile_delete_route(self):
        '''
        Test successful deletion of profile
        '''
        # Admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test User1', password='Test@User1'),
            follow_redirects=True
        )

        response = self.client.get(
            url_for('profile.delete_profile'), 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Home</title>", response.data)
    # ==============================================================================================================
    def test_3_profile_delete_route(self):
        '''
        Test deletion of profile with no login
        '''
        response = self.client.get(
            url_for('profile.delete_profile'), 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    

if __name__ == "__main__":
    unittest.main()