import unittest

from base_test import BaseTestCase

class Test_Main_Pages(BaseTestCase):

    def test_home_page(self):
        '''
        Tests the web app home page
        '''
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Home", response.data)

    def test_manage_page(self):
        '''
        Tests the manage page
        '''
        response = self.client.get("/manage", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Manage", response.data)

    def test_add_page_get(self):
        '''
        Tests the add info page form the default database
        '''
        response = self.client.get("/manage/add_info", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add", response.data)

    def test_404_page(self):
        '''
        Tests the 404 page
        '''
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)

class Test_User_Inputs(BaseTestCase):

    def test_add_page_post(self):
        '''
        Tests the post route for the add page
        '''
        response = self.client.post('/manage/add_info', data={
            'name': 'Test User',
            'date': '2024-05-23',
            'message': 'This is a test message from the unit testing.'
        })
        self.assertEqual(response.status_code, 302)     # Expect Redirect
        self.assertIn(b'manage', response.data)


if __name__ == "__main__":
    unittest.main()