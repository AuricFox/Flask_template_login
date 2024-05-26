import unittest

from base_test import BaseTestCase

from app.forms import default_form, login_form, profile_form, register_form, user_form

# ==============================================================================================================
class Test_Default_Form(BaseTestCase):

    def test_validate_success_form(self):
        '''
        Tests the input for the default form
        '''
        form = default_form(
            name='Test User',
            date='2024-05-23',
            message='This is a test message from the unit testing.'
        )
        self.assertTrue(form.validate())


if __name__ == "__main__":
    unittest.main()