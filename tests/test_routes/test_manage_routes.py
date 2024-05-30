import unittest

from flask import url_for

from tests.base_test import BaseTestCase_Models

# ==============================================================================================================
# TEST MANAGE PAGE
# ==============================================================================================================
class Test_Manage_Page(BaseTestCase_Models):

    def test_manage_page(self):
        '''
        Tests the manage page
        '''
        response = self.client.get(url_for('manage.index'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage</title>", response.data)
# ==============================================================================================================
# TEST ADD PAGE
# ==============================================================================================================
class Test_Add_Page(BaseTestCase_Models):

    def test_1_add_page(self):
        '''
        Tests the add info page form the default database
        '''
        response = self.client.get(url_for('manage.add_info'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Add</title>", response.data)
    # ==============================================================================================================
    def test_2_add_page(self):
        '''
        Tests for a successful post for the add page
        '''
        response = self.client.post(
            url_for('manage.add_info'), 
            data={
                'name': 'Test Name',
                'date': '2024-05-23',
                'message': 'This is a test message from the unit testing.'}, 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Manage</title>', response.data)
    # ==============================================================================================================
    def test_3_add_page(self):
        '''
        Tests for a missing name field when adding data
        '''
        response = self.client.post(
            url_for('manage.add_info'), 
            data={
                'date': '2024-05-23',
                'message': 'This is a test message from the unit testing.'}, 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Add</title>', response.data)
    # ==============================================================================================================
    def test_4_add_page(self):
        '''
        Tests for a missing date field when adding data
        '''
        response = self.client.post(
            url_for('manage.add_info'), 
            data={
                'name': 'Test Name',
                'message': 'This is a test message from the unit testing.'}, 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Manage</title>', response.data)
    # ==============================================================================================================
    def test_5_add_page(self):
        '''
        Tests for a missing message field when adding data
        '''
        response = self.client.post(
            url_for('manage.add_info'), 
            data={
                'name': 'Test Name',
                'date': '2024-05-23'}, 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Manage</title>', response.data)
# ==============================================================================================================
# TEST VIEW PAGE
# ==============================================================================================================
class Test_View_Page(BaseTestCase_Models):

    def test_1_view_page(self):
        '''
        Tests the view page
        '''
        response = self.client.get(url_for('manage.view', id=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>View</title>", response.data)
    # ==============================================================================================================
    def test_2_view_page(self):
        '''
        Tests the view page for invalid id
        '''
        response = self.client.get(url_for('manage.view', id=100), follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
# ==============================================================================================================
# TEST EDIT PAGE
# ==============================================================================================================
class Test_Edit_Page(BaseTestCase_Models):

    def test_1_Update_page(self):
        '''
        Tests the edit page
        '''
        response = self.client.get(url_for('manage.update_info', id=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Edit</title>", response.data)
    # ==============================================================================================================
    def test_2_Update_page(self):
        '''
        Tests the edit page for invalid id
        '''
        response = self.client.get(url_for('manage.update_info', id=100), follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
    # ==============================================================================================================
    def test_3_Update_page(self):
        '''
        Tests the edit page for successful post
        '''
        response = self.client.post(
            url_for('manage.update_info', id=1), 
            data = {
                'name': 'Edit Test',
                'date': '2024-05-30',
                'message': 'This is a test for the edit page'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage</title>", response.data)
    # ==============================================================================================================
    def test_4_Update_page(self):
        '''
        Tests the edit page for posts with invalid ID's
        '''
        response = self.client.post(
            url_for('manage.update_info', id=100), 
            data = {
                'name': 'Edit Test',
                'date': '2024-05-30',
                'message': 'This is a test for the edit page'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
    # ==============================================================================================================
    def test_5_Update_page(self):
        '''
        Tests the edit posts with missing name field
        '''
        response = self.client.post(
            url_for('manage.update_info', id=1), 
            data = {
                'date': '2024-05-30',
                'message': 'This is a test for the edit page'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Edit</title>", response.data)
    # ==============================================================================================================
    def test_6_Update_page(self):
        '''
        Tests the edit posts with missing date field
        '''
        response = self.client.post(
            url_for('manage.update_info', id=1), 
            data = {
                'name': 'Edit Test',
                'message': 'This is a test for the edit page'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage</title>", response.data)
    # ==============================================================================================================
    def test_7_Update_page(self):
        '''
        Tests the edit posts with missing message field
        '''
        response = self.client.post(
            url_for('manage.update_info', id=1), 
            data = {
                'name': 'Edit Test',
                'date': '2024-05-30'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage</title>", response.data)
# ==============================================================================================================
# TEST DELETE PAGE
# ==============================================================================================================
class Test_Delete_Route(BaseTestCase_Models):

    def test_1_delete_route(self):
        '''
        Tests the delete route
        '''
        response = self.client.get(url_for('manage.delete', id=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage</title>", response.data)
    # ==============================================================================================================
    def test_2_delete_route(self):
        '''
        Tests the delete route for invalid id
        '''
        response = self.client.get(url_for('manage.delete', id=100), follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<title>Page Not Found</title>", response.data)


if __name__ == "__main__":
    unittest.main()