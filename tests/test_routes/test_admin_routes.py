import unittest

from flask import url_for
from flask_login import current_user

from tests.base_test import BaseTestCase_User

class Test_Admin_Pages(BaseTestCase_User):

    def test_manage_usgers_page(self):
        '''
        Tests the successful navigation for the manage users page
        '''
        with self.client:

            response = self.client.post(
                url_for('auth.login'), 
                data = dict(username='Test Admin', password='Test@Admin1'),
                follow_redirects=True
            )

            response = self.client.get("/admin", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertIn(b"Manage Users", response.data)


if __name__ == "__main__":
    unittest.main()