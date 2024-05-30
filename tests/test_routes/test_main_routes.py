import unittest

from tests.base_test import BaseTestCase

class Test_Main_Pages(BaseTestCase):

    def test_home_page(self):
        '''
        Tests the web app home page
        '''
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Home", response.data)
    # ==============================================================================================================
    def test_404_page(self):
        '''
        Tests the 404 page
        '''
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)
        

if __name__ == "__main__":
    unittest.main()