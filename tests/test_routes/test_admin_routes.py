import unittest

from flask import url_for
from flask_login import current_user

from tests.base_test import BaseTestCase_User

# ==============================================================================================================
# TEST MAIN ADMIN PAGE
# ==============================================================================================================
class Test_Admin_Page(BaseTestCase_User):

    def test_1_admin_page(self):
        '''
        Tests the manage users page with successful login
        '''

        # Admin Login
        response = self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )

        response = self.client.get("/admin", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Manage Users</title>", response.data)
    # ==============================================================================================================
    def test_2_admin_page(self):
        '''
        Tests the manage users page with no login
        '''
        response = self.client.get("/admin", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    # ==============================================================================================================
    def test_3_admin_page(self):
        '''
        Tests the manage users page with non-admin users
        '''

        # Admin Login
        response = self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test User1', password='Test@User1'),
            follow_redirects=True
        )

        response = self.client.get("/admin", follow_redirects=True)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
# ==============================================================================================================
# TEST ADMIN VIEW PAGE
# ==============================================================================================================
class Test_Admin_View_Page(BaseTestCase_User):

    def test_1_admin_view_page(self):
        '''
        Tests the admin view page with login
        '''
        # Admin Login
        response = self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )        

        response = self.client.get(url_for('admin.view_user', id=1), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>View User</title>", response.data)
    # ==============================================================================================================
    def test_2_admin_view_page(self):
        '''
        Tests the admin view page with no login
        '''
        response = self.client.get(url_for('admin.view_user', id=1), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    # ==============================================================================================================
    def test_3_admin_view_page(self):
        '''
        Tests the view page for invalid id
        '''
        # Admin Login
        response = self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )

        response = self.client.get(url_for('admin.view_user', id=100), follow_redirects=True)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
    # ==============================================================================================================
    def test_4_admin_view_page(self):
        '''
        Tests the view page for invalid id with no login
        '''
        response = self.client.get(url_for('admin.view_user', id=100), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    # ==============================================================================================================
    def test_5_admin_view_page(self):
        '''
        Tests the admin view page with non-admin user
        '''
        # Admin Login
        response = self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test User1', password='Test@User1'),
            follow_redirects=True
        )        

        response = self.client.get(url_for('admin.view_user', id=1), follow_redirects=True)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
# ==============================================================================================================
# TEST ADMIN UPDATE PAGE
# ==============================================================================================================
class Test_Admin_Update_Page(BaseTestCase_User):

    def test_1_admin_update_page(self):
        '''
        Tests the admin update page with login
        '''
        # Admin Login
        response = self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )        

        response = self.client.get(url_for('admin.update_user', id=1), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Edit User</title>", response.data)
    # ==============================================================================================================
    def test_2_admin_update_page(self):
        '''
        Tests the admin update page without login
        '''
        response = self.client.get(url_for('admin.update_user', id=1), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    # ==============================================================================================================
    def test_3_admin_update_page(self):
        '''
        Tests the admin update post with login
        '''
        # Admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )        

        response = self.client.post(
            url_for('admin.update_user', id=1), 
            data={
                'id': '1',
                'username': 'Update User',
                'email': 'updateuser@testing.com',
                'password': 'Update@user1',
                'confirm': 'Update@user1',
                'is_admin': False
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Manage Users</title>", response.data)
    # ==============================================================================================================
    def test_4_admin_update_page(self):
        '''
        Tests the admin update post without login
        '''
        response = self.client.post(
            url_for('admin.update_user', id=1), 
            data={
                'id': '1',
                'username': 'Update User',
                'email': 'updateuser@testing.com',
                'password': 'Update@user1',
                'confirm': 'Update@user1',
                'is_admin': False
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    # ==============================================================================================================
    def test_5_admin_update_page(self):
        '''
        Tests the admin update post with missing optional fields
        '''
        # Admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )        

        response = self.client.post(
            url_for('admin.update_user', id=1), 
            data={
                'id': '1'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Manage Users</title>", response.data)
    # ==============================================================================================================
    def test_6_admin_update_page(self):
        '''
        Tests the admin update post with non-admin user
        '''
        # Admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test User1', password='Test@User1'),
            follow_redirects=True
        )        

        response = self.client.post(
            url_for('admin.update_user', id=1), 
            data={
                'id': '1',
                'username': 'Update User',
                'email': 'updateuser@testing.com',
                'password': 'Update@user1',
                'confirm': 'Update@user1',
                'is_admin': False
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
# ==============================================================================================================
# TEST ADMIN DELETE ROUTE
# ==============================================================================================================
class Test_Admin_Delete_Route(BaseTestCase_User):

    def test_1_admin_delete_route(self):
        '''
        Test successful deletion of a user
        '''
        # Admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test Admin', password='Test@Admin1'),
            follow_redirects=True
        )

        response = self.client.get(
            url_for('admin.delete_user', id=1), 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Manage Users</title>", response.data)
    # ==============================================================================================================
    def test_2_admin_delete_route(self):
        '''
        Test deletion of a user with non-admin login
        '''
        # Non-admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test User1', password='Test@User1'),
            follow_redirects=True
        )

        response = self.client.get(
            url_for('admin.delete_user', id=1), 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
    # ==============================================================================================================
    def test_3_admin_delete_route(self):
        '''
        Test deletion of a user with no login
        '''
        response = self.client.get(
            url_for('admin.delete_user', id=1), 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b"<title>Login</title>", response.data)
    # ==============================================================================================================
    def test_4_admin_delete_route(self):
        '''
        Test deletion of a user with invalid user ID
        '''
        # Admin Login
        self.client.post(
            url_for('auth.login'), 
            data = dict(username='Test User1', password='Test@User1'),
            follow_redirects=True
        )

        response = self.client.get(
            url_for('admin.delete_user', id=100), 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b"<title>Page Not Found</title>", response.data)


if __name__ == "__main__":
    unittest.main()